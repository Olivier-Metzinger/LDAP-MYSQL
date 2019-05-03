# coding=utf-8
import os
import ldap
import smtplib
import logging
import ldap.modlist
import mysql.connector
from datetime import datetime
from email.mime.text import MIMEText
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE


def prYellow(skk): print("\033[96m {}\033[00m".format(skk))


def prGreen(skk): print("\033[92m {}\033[00m".format(skk))


def prRed(skk): print("\033[91m {}\033[00m".format(skk))


logging.basicConfig(filename='error_log.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s  --  %(pathname)s  --  %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', )

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
        prGreen("Utilisateur ajouté : LID : {}".format(row[15]))
    except:
        try:
            old_value = {"uid": [""], "Actif": [""], "DateFinActif": [""],
                         "cn": [""], "sn": [""]}

            new_value = {"uid": ["{}".format(row[14])], "Actif": ["1"],
                         "DateFinActif": ["{}".format(row[19])],
                         "cn": ["{}".format(row[21].encode("utf-8"))], "sn": ["{}".format(row[21].encode("utf-8"))]}

            modlist = ldap.modlist.modifyModlist(old_value, new_value)
            load.modify_s(dn, modlist)
            prGreen("Utilisateur modifié : LID : {}".format(row[15]))
        except:
            logging.error('Fail to ADD and/or MODIFY user LID:{LID} | NAME: {NAME}\n'.format(LID=row[15], NAME=row[21]))


#############REQUÊTES ENTREPRISES ET ASSURÉS#######################

def query(mydb, load):
    EntreprisesQuery = "SELECT * FROM RoedererEntreprises.SBYN_SYSTEMSBR INNER JOIN RoedererEntreprises.SBYN_ENTERPRISE ON SBYN_SYSTEMSBR.EUID = SBYN_ENTERPRISE.EUID INNER JOIN RoedererEntreprises.SBYN_ENTERPRISE_DETAIL ON SBYN_ENTERPRISE_DETAIL.LID = SBYN_ENTERPRISE.LID AND SBYN_ENTERPRISE_DETAIL.SYSTEMCODE = SBYN_ENTERPRISE.SYSTEMCODE WHERE SBYN_ENTERPRISE_DETAIL.SYSTEMCODE = 'AS400' AND SBYN_SYSTEMSBR.UPDATEDATE >= '{}'".format(
        synchro)
    cursor = mydb.cursor()
    cursor.execute(EntreprisesQuery)
    records_Entreprises = cursor.fetchall()

    PersonnesQuery = "SELECT * FROM RoedererPersonnes.SBYN_SYSTEMSBR INNER JOIN RoedererPersonnes.SBYN_ENTERPRISE ON SBYN_SYSTEMSBR.EUID = SBYN_ENTERPRISE.EUID INNER JOIN RoedererPersonnes.SBYN_ENTERPRISE_DETAIL ON SBYN_ENTERPRISE_DETAIL.LID = SBYN_ENTERPRISE.LID AND SBYN_ENTERPRISE_DETAIL.SYSTEMCODE = SBYN_ENTERPRISE.SYSTEMCODE WHERE SBYN_ENTERPRISE_DETAIL.SYSTEMCODE = 'AS400' AND SBYN_SYSTEMSBR.UPDATEDATE >= '2019-05-03 08:20:58'".format(
        synchro)
    cursor = mydb.cursor()
    cursor.execute(PersonnesQuery)
    records_Personnes = cursor.fetchall()

    #############LECTURE DES DONNÉES REQUÊTE##########################

    prRed("MODIFICATION ENTREPRISES")
    for row in records_Entreprises:
        if (row[17] == "ROEDERER"):
            dn = "LID={},ou=Entreprise,ou=Roederer,dc=roederer,dc=fr".format(row[15])
        elif (row[17] == "SIMAX"):
            dn = "LID={},ou=Entreprise,ou=Simax Santé,dc=roederer,dc=fr".format(row[15])
        else:
            continue
        add_user(load, row, dn)

    prRed("MODIFICATION ASSURÉS")
    for row2 in records_Personnes:
        if (row2[17] == "ROEDERER"):
            dn = "LID={},ou=Assuré,ou=Roederer,dc=roederer,dc=fr".format(row2[15])
        elif (row2[17] == "SIMAX"):
            dn = "LID={},ou=Assuré,ou=Simax,dc=roederer,dc=fr".format(row2[15])
        else:
            continue
        add_user(load, row2, dn)
    send_log()


def send_log():
    fp = open('error_log.log', 'rb')
    msg = MIMEText(fp.read())
    fp.close()
    msg['Subject'] = 'ERROR SYNC LDAP'
    msg['From'] = 'pole-web@roederer.fr'
    msg['To'] = 'pole-web@roederer.fr'
    if (os.stat("error_log.log").st_size) > 0:
        server = smtplib.SMTP('10.10.44.148')
        server.sendmail("pole-web@roederer.fr", "pole-web@roederer.fr", msg.as_string())
