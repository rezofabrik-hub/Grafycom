#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Expedition de courriel en SMTP, partagee par les outils du depot.

Les identifiants ne sont pas ici et n'y seront jamais : ils sont lus dans
l'environnement, ou l'hebergeur les garde chiffres.

    GRAFYCOM_SMTP_UTILISATEUR   l'adresse expeditrice
    GRAFYCOM_SMTP_MOTDEPASSE    un mot de passe d'application

Avec Gmail, le mot de passe du compte ne marche pas : il faut un mot de
passe d'application. C'est une bonne chose — celui-la ne donne que le
droit d'envoyer, et se revoque sans toucher au compte.

Voir outils/VEILLE-QUOTIDIENNE.md pour la procedure complete.
"""
import os
import smtplib
from email.message import EmailMessage

HOTE = os.environ.get("GRAFYCOM_SMTP_HOTE", "smtp.gmail.com")
PORT = int(os.environ.get("GRAFYCOM_SMTP_PORT", "587"))

MANQUE = (
    "identifiants d'envoi absents. Renseigner GRAFYCOM_SMTP_UTILISATEUR "
    "(l'adresse expeditrice) et GRAFYCOM_SMTP_MOTDEPASSE (un mot de passe "
    "d'application, pas le mot de passe du compte) dans les variables "
    "d'environnement. Voir outils/VEILLE-QUOTIDIENNE.md."
)


def identifiants() -> tuple[str, str]:
    """Le couple (utilisateur, secret). Leve si l'un des deux manque."""
    utilisateur = os.environ.get("GRAFYCOM_SMTP_UTILISATEUR", "").strip()
    secret = os.environ.get("GRAFYCOM_SMTP_MOTDEPASSE", "").strip()
    if not utilisateur or not secret:
        raise RuntimeError(MANQUE)
    return utilisateur, secret


def envoyer(destinataires: list[str], copie: list[str], sujet: str,
            html: str, texte: str) -> None:
    """Expedie un courriel en deux versions. Leve si l'envoi echoue.

    Le repli texte n'est pas une politesse : certains clients de
    messagerie, et tous les lecteurs d'ecran, ne lisent que celui-la.
    """
    utilisateur, secret = identifiants()

    msg = EmailMessage()
    msg["From"] = utilisateur
    msg["To"] = ", ".join(destinataires)
    if copie:
        msg["Cc"] = ", ".join(copie)
    msg["Subject"] = sujet
    msg.set_content(texte)
    msg.add_alternative(html, subtype="html")

    with smtplib.SMTP(HOTE, PORT, timeout=60) as serveur:
        serveur.starttls()
        serveur.login(utilisateur, secret)
        serveur.send_message(msg, to_addrs=destinataires + copie)


def liste(valeur: str) -> list[str]:
    """Decoupe une chaine d'adresses separees par des virgules."""
    return [x.strip() for x in (valeur or "").split(",") if x.strip()]
