#!/usr/bin/env python3
"""Fait pointer grafycom.fr (sans www) vers GitHub Pages, dans Route 53.

Aujourd'hui seul grafycom.fr résout : quelqu'un qui tape « grafycom.fr »
dans sa barre d'adresse tombe sur une erreur. Il manque quatre
enregistrements A sur le domaine nu. GitHub redirige ensuite tout seul vers
www, puisque c'est lui le domaine personnalisé du dépôt.

Le script peut être relancé sans dommage : il écrit
l'état voulu plutôt qu'il n'ajoute, et ne touche à rien si c'est déjà bon.

Il lui faut des identifiants AWS ayant le droit de lire les zones et de
modifier celle-ci :
    route53:ListHostedZones, route53:ChangeResourceRecordSets,
    route53:ListResourceRecordSets, route53:GetChange

    python3 outils/dns-apex.py              # montre ce qui serait fait
    python3 outils/dns-apex.py --appliquer  # le fait
"""

from __future__ import annotations

import argparse
import os
import sys
import time

DOMAINE = "grafycom.fr"
# Les adresses de GitHub Pages pour les domaines nus. Les AAAA servent
# aux visiteurs en IPv6 — chez Free et sur les réseaux mobiles français,
# ce n'est plus une minorité.
CIBLES = {
    "A": ["185.199.108.153", "185.199.109.153",
          "185.199.110.153", "185.199.111.153"],
    "AAAA": ["2606:50c0:8000::153", "2606:50c0:8001::153",
             "2606:50c0:8002::153", "2606:50c0:8003::153"],
}
TTL = 300


def identifiants() -> dict:
    """Les clés à présenter à AWS.

    Dans l'environnement d'exécution de Claude, AWS_ACCESS_KEY_ID et
    AWS_SECRET_ACCESS_KEY sont déjà occupés : le proxy y injecte la valeur
    « proxy-injected », qui n'est pas un identifiant. Une clé déposée sous
    ces noms-là risque donc d'être écrasée sans bruit.

    On regarde d'abord une paire à soi, GRAFYCOM_AWS_*, qui n'entre en
    collision avec rien. À défaut, on laisse boto3 chercher comme il en a
    l'habitude — ce qui convient sur une machine où la configuration AWS
    est normale.
    """
    cle = os.environ.get("GRAFYCOM_AWS_ACCESS_KEY_ID")
    secret = os.environ.get("GRAFYCOM_AWS_SECRET_ACCESS_KEY")
    if cle and secret:
        print("Identifiants : GRAFYCOM_AWS_*")
        return {"aws_access_key_id": cle, "aws_secret_access_key": secret}
    if os.environ.get("AWS_ACCESS_KEY_ID") == "proxy-injected":
        print("Attention : AWS_ACCESS_KEY_ID vaut « proxy-injected », ce qui "
              "n'est pas\nun identifiant. Déposez la clé sous "
              "GRAFYCOM_AWS_ACCESS_KEY_ID et\nGRAFYCOM_AWS_SECRET_ACCESS_KEY.",
              file=sys.stderr)
    return {}


def main() -> int:
    a = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--appliquer", action="store_true",
                   help="écrire réellement ; sans cette option, rien n'est modifié")
    args = a.parse_args()

    try:
        import boto3
        from botocore.exceptions import ClientError, NoCredentialsError
    except ImportError:
        print("boto3 manquant :  pip install boto3", file=sys.stderr)
        return 1

    r53 = boto3.client("route53", region_name="us-east-1", **identifiants())

    try:
        zones = [z for z in r53.list_hosted_zones()["HostedZones"]
                 if z["Name"].rstrip(".") == DOMAINE and not z["Config"].get("PrivateZone")]
    except (ClientError, NoCredentialsError) as e:
        code = getattr(e, "response", {}).get("Error", {}).get("Code", type(e).__name__)
        print(f"AWS refuse la connexion ({code}).", file=sys.stderr)
        print("Vérifiez GRAFYCOM_AWS_ACCESS_KEY_ID et "
              "GRAFYCOM_AWS_SECRET_ACCESS_KEY.", file=sys.stderr)
        return 1

    if not zones:
        print(f"Aucune zone publique « {DOMAINE} » sur ce compte.", file=sys.stderr)
        return 1
    if len(zones) > 1:
        print(f"Plusieurs zones « {DOMAINE} » : à démêler à la main.", file=sys.stderr)
        return 1

    zone = zones[0]
    zid = zone["Id"].split("/")[-1]
    print(f"Zone {DOMAINE} ({zid})")

    actuels: dict[str, list[str]] = {t: [] for t in CIBLES}
    lots = r53.get_paginator("list_resource_record_sets")
    for lot in lots.paginate(HostedZoneId=zid):
        for r in lot["ResourceRecordSets"]:
            if r["Name"].rstrip(".") == DOMAINE and r["Type"] in CIBLES:
                actuels[r["Type"]] = [v["Value"] for v in r.get("ResourceRecords", [])]

    a_faire = [t for t in CIBLES if sorted(actuels[t]) != sorted(CIBLES[t])]
    for t in CIBLES:
        etat = "déjà bon" if t not in a_faire else (
            ", ".join(actuels[t]) if actuels[t] else "absent")
        print(f"  {t:5s} {etat}")

    if not a_faire:
        print("\nTout est déjà en place. Rien à faire.")
        return 0

    print("\nÀ écrire :", ", ".join(a_faire))
    if not args.appliquer:
        print("Essai à blanc. Relancer avec --appliquer pour écrire.")
        return 0

    reponse = r53.change_resource_record_sets(
        HostedZoneId=zid,
        ChangeBatch={
            "Comment": "Domaine nu vers GitHub Pages",
            "Changes": [{
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": DOMAINE,
                    "Type": t,
                    "TTL": TTL,
                    "ResourceRecords": [{"Value": ip} for ip in CIBLES[t]],
                },
            } for t in a_faire],
        },
    )

    change = reponse["ChangeInfo"]["Id"].split("/")[-1]
    print(f"\nModification envoyée ({change}). Attente de la propagation…")
    for _ in range(40):
        etat = r53.get_change(Id=change)["ChangeInfo"]["Status"]
        if etat == "INSYNC":
            print("Propagé sur tous les serveurs Route 53.")
            break
        time.sleep(15)
    else:
        print("Toujours en cours après dix minutes — vérifiez dans la console.")

    print("\nÀ vérifier dans l'heure qui suit :")
    print(f"  curl -sI https://{DOMAINE}/     → doit rediriger vers www")
    print("  GitHub peut mettre jusqu'à une heure à émettre le certificat du")
    print("  domaine nu. Si « Enforce HTTPS » se décoche, le recocher après.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
