# coding=utf-8
import ldap
import ldap.modlist
import mysql.connector
from datetime import datetime
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE


def prGreen(skk): print("\033[92m {}\033[00m".format(skk))


def prRed(skk): print("\033[91m {}\033[00m".format(skk))


import time


synchro = datetime(2019, 5, 2, 10, 16, 4)  # Y, M, D, h, m, s


def add_user(load, row, dn):
    date = datetime.now()
    modlistadd = {
        "objectClass": ["RoedererClass", "inetOrgPerson"],
        "LID": ["{}".format(row[15])],
        "uid": ["{}".format(row[14])],
        "Actif": ["1"],
        "DateFinActif": ["{}".format(row[19])],
        "DateMajMdp": ["{}".format(date)],
        "userPassword": ["{}".format(row[20])],
        "MdpInitial": ["Non"],
        "cn": ["{}".format(row[21].encode("utf-8"))],
        "sn": ["{}".format(row[21].encode("utf-8"))],
    }

    try:
        load.add_s(dn, ldap.modlist.addModlist(modlistadd))
        prGreen("Utilisateur ajouté")
    except:
        old_value = {"uid": [""], "Actif": [""], "DateFinActif": [""], "DateMajMdp":[""],
                     "MdpInitial": [""], "cn": [""], "sn": [""]}

        new_value = {"uid": ["{}".format(row[14])], "Actif": ["1"],
                     "DateFinActif": ["{}".format(row[19])], "DateMajMdp": ["{}".format(date)],
        "MdpInitial": ["Non"], "cn": ["{}".format(row[21].encode("utf-8"))], "sn": ["{}".format(row[21].encode("utf-8"))]}

        modlist = ldap.modlist.modifyModlist(old_value, new_value)
        load.modify_s(dn, modlist)
        prGreen("Utilisateur modifié")


def query(mydb, load):
    EntreprisesQuery = "SELECT * FROM RoedererEntreprises.SBYN_SYSTEMSBR INNER JOIN RoedererEntreprises.SBYN_ENTERPRISE ON SBYN_SYSTEMSBR.EUID = SBYN_ENTERPRISE.EUID INNER JOIN RoedererEntreprises.SBYN_ENTERPRISE_DETAIL ON SBYN_ENTERPRISE_DETAIL.LID = SBYN_ENTERPRISE.LID AND SBYN_ENTERPRISE_DETAIL.SYSTEMCODE = SBYN_ENTERPRISE.SYSTEMCODE WHERE SBYN_ENTERPRISE_DETAIL.SYSTEMCODE = 'AS400' AND SBYN_SYSTEMSBR.UPDATEDATE >= '{}'".format(
        synchro)
    cursor = mydb.cursor()
    cursor.execute(EntreprisesQuery)
    records_Entreprises = cursor.fetchall()

    PersonnesQuery = "SELECT * FROM RoedererEntreprises.SBYN_SYSTEMSBR INNER JOIN RoedererEntreprises.SBYN_ENTERPRISE ON SBYN_SYSTEMSBR.EUID = SBYN_ENTERPRISE.EUID INNER JOIN RoedererEntreprises.SBYN_ENTERPRISE_DETAIL ON SBYN_ENTERPRISE_DETAIL.LID = SBYN_ENTERPRISE.LID AND SBYN_ENTERPRISE_DETAIL.SYSTEMCODE = SBYN_ENTERPRISE.SYSTEMCODE WHERE SBYN_ENTERPRISE_DETAIL.SYSTEMCODE = 'AS400' AND SBYN_SYSTEMSBR.UPDATEDATE <= '{}' LIMIT 1".format(
        synchro)
    cursor = mydb.cursor()
    cursor.execute(PersonnesQuery)
    records_Personnes = cursor.fetchall()

    ####CAS ENTREPRISE ########

    for row in records_Entreprises:
        if (row[17] == "ROEDERER"):
            dn = "LID={},ou=Entreprise,ou=Roederer,dc=roederer,dc=fr".format(row[15])
        elif (row[17] == "SIMAX"):
            dn = "LID={},ou=Entreprise,ou=Simax Santé,dc=roederer,dc=fr".format(row[15])
        else:
            continue

        add_user(load, row, dn)


    ####CAS PERSONNES ########
    #
    # for row2 in records_Personnes:
    #     if (row2[17] == "ROEDERER"):
    #         dn = "LID={},ou=Entreprise,ou=Roederer,dc=roederer,dc=fr".format(row2[15])
    #     elif (row2[17] == "SIMAX"):
    #         dn = "LID={},ou=Entreprise,ou=Simax,dc=roederer,dc=fr".format(row2[15])
    #     else:
    #         continue
    #     add_user(load, row, dn)
    #print("Total de rows : ", cursor.rowcount)
