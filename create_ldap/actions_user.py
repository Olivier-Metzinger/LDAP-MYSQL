#!/usr/bin/python
# coding=utf-8

import time
import ldap
import logging
from datetime import datetime


def add_user(server, row, dn):
    date = datetime.now()
    modlistadd = {
        "objectClass": ["ROEDECLASS", "inetOrgPerson"],
        "LID": ["{}".format(str(row['LID']))],                      #LISTE DES CLASS ET ATTRIBUTS POUR L'AJOUT UTILISATEUR
        "uid": ["{}".format(str(row['EUID']))],
        "Actif": ["1"],
        "DateFinActif": ["{}".format(str(row['DTFIN']))],
        "DateMajMdp": ["{}".format(date)],
        "userPassword": ["{}".format(str(row['PASS']))],
        "MdpInitial": ["Non"],
        "cn": ["{}".format(str(row['NOM'].encode("utf-8")))],
        "sn": ["{}".format(str(row['NOM'].encode("utf-8")))],
    }
    try:
        server.add_s(dn, ldap.modlist.addModlist(modlistadd))
        print("Utilisateur ajouté {} | {}".format(str(row['LID'].encode("utf-8")), str(row['NOM'].encode("utf-8"))))
    except AssertionError as error:
        print(error)


def add_group(server, row, dn):
    modlistgroup = {
        "objectClass": ["organizationalUnit"],
        "description": ["{}".format(str(row['NOM'].encode("utf-8")))],      #LISTE DES CLASS ET ATTRIBUTS POUR L'AJOUT GROUPE ENTREPRISE
    }
    try:
        server.add_s(dn, ldap.modlist.addModlist(modlistgroup))
        print("Groupe ajouté : {} | {}".format(str(row['LID']), str(row['NOM'].encode("utf-8"))))
    except AssertionError as error:
        print(error)


def add_base(server, dn):
    modlistbase = {
        "objectClass": ["organizationalUnit"],
    }
    try:
        server.add_s(dn, ldap.modlist.addModlist(modlistbase))          #LISTE POUR L'ARCHITECTURE DE BASE
        print("Branche ajoutée")
    except AssertionError as error:
        print(error)


def add_apporteurs(server, row, dn):
    modlistapport = {
        "objectClass": ["ROEDCLASS", "inetOrgPerson"],
        "LID": ["{}".format(str(row['LID'].encode("utf-8")))],
        "Actif": ["1"],                                                 #LISTE DES CLASS ET ATTRIBUTS POUR L'AJOUT APPORTEURS
        "userPassword": ["{}".format(str(row['PASS']))],
        "cn": ["{}".format(str(row['LID'].encode("utf-8")))],
        "sn": ["{}".format(str(row['LID'].encode("utf-8")))],
    }
    try:
        server.add_s(dn, ldap.modlist.addModlist(modlistapport))
        print("Apporteur ajouté {}".format(str(row['LID'].encode("utf-8"))))
    except AssertionError as error:
        print(error)
