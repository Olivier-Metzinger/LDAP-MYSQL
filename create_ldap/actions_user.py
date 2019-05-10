#!/usr/bin/python
# coding=utf-8

import time
import ldap
import logging
from datetime import datetime

result = 0

def add_user(server, row, dn):
    global result
    date = datetime.now()
    modlistadd = {
        "objectClass": ["RoedererClass", "inetOrgPerson"],
        "LID": ["{}".format(str(row['LID']))],
        "uid": ["{}".format(str(row['EUID']))],
        "Actif": ["1"],
        "DateFinActif": ["{}".format(str(row['DTFIN']))],
        "DateMajMdp": ["{}".format(date)],
        "userPassword": ["{}".format(str(row['PASS']))],
        "MdpInitial": ["Non"],
        "cn": ["{}".format(str(row['NOM'].encode("utf-8")))],
        "sn": ["{}".format(str(row['NOM'].encode("utf-8")))],
    }
    result = result + 1
    try:
        server.add_s(dn, ldap.modlist.addModlist(modlistadd))
        print("Utilisateur ajouté {} | {}".format(str(row['LID']), str(row['NOM'])))
    except AssertionError as error:
        print(error)


def add_group(server, row, dn):
    modlistgroup = {
        "objectClass": ["organizationalUnit"],
        "description": ["{}".format(str(row['NOM']))],
    }
    try:
        server.add_s(dn, ldap.modlist.addModlist(modlistgroup))
        print("Groupe ajouté : {} | {}".format(str(row['LID']), str(row['NOM'])))
    except AssertionError as error:
        print(error)


def add_base(server, dn):
    modlistbase = {
        "objectClass": ["organizationalUnit"],
    }
    try:
        server.add_s(dn, ldap.modlist.addModlist(modlistbase))
        print("Branche ajoutée")
    except AssertionError as error:
        print(error)


def add_apporteurs(server, row, dn):
    global result
    modlistapport = {
        "objectClass": ["RoedererClass", "inetOrgPerson"],
        "LID": ["{}".format(str(row['LID']))],
        "Actif": ["1"],
        "userPassword": ["{}".format(str(row['PASS']))],
        "cn": ["{}".format(str(row['LID'].encode("utf-8")))],
        "sn": ["{}".format(str(row['LID'].encode("utf-8")))],
    }
    result = result + 1
    try:
        server.add_s(dn, ldap.modlist.addModlist(modlistapport))
        print("Appoteur ajouté {}".format(str(row['LID'])))
    except AssertionError as error:
        print(error)