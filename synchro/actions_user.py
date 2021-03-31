# coding=utf-8

import time
import ldap
import logging
from datetime import datetime

def prGreen(skk): print("\033[92m {}\033[00m".format(skk))

def add_group(server, row, dn):
    modlistgroup = {
        "objectClass": ["organizationalUnit"],
        "description": ["{}".format(str(row['NAME']))],
    }
    try:
        server.add_s(dn, ldap.modlist.addModlist(modlistgroup))
        prGreen("Groupe entreprise ajouté : LID : {} | NOM : {} | GESTIONNAIRE : {}".format(str(row['LID']), str(row['NAME']), str(row['GESTIONNAIRE'])))
    except AssertionError as error:
        print(error)

def add_user(server, row, dn):
    date = datetime.now()
    modlistadd = {
        "objectClass": ["Roed", "inetOrgPerson"],
        "LID": ["{}".format(str(row['LID']))],
        "uid": ["{}".format(str(row['EUID']))],
        "Actif": ["1"],
        "DateFinActif": ["{}".format(str(row['DTFIN']))],
        "DateMajMdp": ["{}".format(date)],
        "userPassword": ["{}".format(str(row['PASSWORD']))],
        "MdpInitial": ["Non"],
        "cn": ["{}".format(str(row['NAME'].encode("utf-8")))],
        "sn": ["{}".format(str(row['NAME'].encode("utf-8")))],
    }
    try:
        server.add_s(dn, ldap.modlist.addModlist(modlistadd))
        prGreen("Utilisateur ajouté : LID : {} | NOM : {} | GESTIONNAIRE : {}".format(str(row['LID']), str(row['NAME']), str(row['GESTIONNAIRE'])))
    except ldap.LDAPError,e:
        print(e)
        logging.error('Fail to ADD and/or MODIFY user LID : {} | NAME : {} | GESTIONNAIRE : {}"\n'.format(str(row['LID']), str(row['NAME']), str(row['GESTIONNAIRE'])))


def modify_user(server, row, dn):
    try:
        old_value = {
            "uid": [""],
            "Actif": [""],
            "DateFinActif": [""],
            "cn": [""],
            "sn": [""]
        }
        new_value = {
            "uid": ["{}".format(str(row['EUID']))],
            "Actif": ["1"],
            "DateFinActif": ["{}".format(str(row['DTFIN']))],
            "cn": ["{}".format(str(row['NAME'].encode("utf-8")))],
            "sn": ["{}".format(str(row['NAME'].encode("utf-8")))]
        }
        modlist = ldap.modlist.modifyModlist(old_value, new_value)
        server.modify_s(dn, modlist)
        prGreen("Utilisateur modifié : LID : {} | NAME : {} | GESTIONNAIRE : {}".format(str(row['LID']), str(row['NAME']), str(row['GESTIONNAIRE'])))
    except ldap.LDAPError:
        logging.error(
            'Fail to ADD and/or MODIFY user LID : {} | NAME : {}\n'.format(str(row['LID']), str(row['NAME'])))
