#!/usr/bin/python
# coding=utf-8

import ldap
import ldap.modlist
import mysql.connector
from datetime import datetime
import time

result = 0


def prGreen(skk): print("\033[92m {}\033[00m".format(skk))


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
        print("User added")
    except AssertionError as error:
        print(error)


def add_group(server, row, dn):
    modlistgroup = {
        "objectClass": ["organizationalUnit"],
        "description": ["{}".format(str(row['NOM']))],
    }
    try:
        server.add_s(dn, ldap.modlist.addModlist(modlistgroup))
        print("Group added")
    except AssertionError as error:
        print(error)


def add_base(server, dn):
    modlistbase = {
        "objectClass": ["organizationalUnit"],
    }
    try:
        server.add_s(dn, ldap.modlist.addModlist(modlistbase))
        print("Group added")
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
        print("user added")
    except AssertionError as error:
        print(error)


def query(mydb, server):
    EntreprisesQuery = "SELECT s1.LID, s1.GESTIONNAIRE, s1.DTFIN, s1.ISACTIVE, s3.PASS, s1.RAISONSOCIALE AS NOM, s1.SYSTEMCODE, s2.EUID FROM RoedererEntreprises.SBYN_ENTERPRISE_DETAIL s1 INNER JOIN TMP_SITEWEB_USER s3 ON s1.LID = s3.LID INNER JOIN SBYN_ENTERPRISE s2 ON s1.LID = s2.LID AND s1.SYSTEMCODE = s2.SYSTEMCODE WHERE s1.SYSTEMCODE = 'AS400' AND s1.GESTIONNAIRE = 'ROEDERER' OR s1.GESTIONNAIRE = 'SIMAX' LIMIT 100;"
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(EntreprisesQuery)
    records_Entreprises = cursor.fetchall()

    PersonnesQuery = "SELECT s1.LID, s1.SYSTEMCODE, s1.GESTIONNAIRE, s1.ISACTIVE, s3.PASS, s1.DTFIN, s1.NOM, s2.EUID FROM RoedererPersonnes.SBYN_ENTERPRISE_DETAIL s1 INNER JOIN RoedererEntreprises.TMP_SITEWEB_USER s3 ON s1.LID = s3.LID INNER JOIN RoedererPersonnes.SBYN_ENTERPRISE s2 ON s1.LID = s2.LID AND s1.SYSTEMCODE = s2.SYSTEMCODE WHERE s1.SYSTEMCODE = 'AS400' AND s1.GESTIONNAIRE = 'ROEDERER' OR s1.GESTIONNAIRE = 'SIMAX' LIMIT 100;"
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(PersonnesQuery)
    records_Personnes = cursor.fetchall()

    ApporteursQuery = "SELECT ID_USER AS LID, GESTIONNAIRE, PASS, TYPE_USER, LID FROM RoedererEntreprises.TMP_SITEWEB_USER WHERE TYPE_USER = 'app';"
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(ApporteursQuery)
    records_Apporteurs = cursor.fetchall()

    data_to_ldap(records_Entreprises, records_Personnes, records_Apporteurs, server)


def data_to_ldap(records_Entreprises, records_Personnes, records_Apporteurs, server):
    prGreen("CRÉATION DE L'ARBRE LDAP...")
    time.sleep(3)
    dn = "ou=Roederer,dc=roederer,dc=fr"
    add_base(server, dn)
    dn1 = "ou=Assurés,ou=Roederer,dc=roederer,dc=fr"
    add_base(server, dn1)
    dn2 = "ou=Entreprises,ou=Roederer,dc=roederer,dc=fr"
    add_base(server, dn2)

    dn3 = "ou=Simax Santé,dc=roederer,dc=fr"
    add_base(server, dn3)
    dn4 = "ou=Assurés,ou=Simax Santé,dc=roederer,dc=fr"
    add_base(server, dn4)
    dn5 = "ou=Entreprises,ou=Simax Santé,dc=roederer,dc=fr"
    add_base(server, dn5)

    dn6 = "ou=Simax Gestion,dc=roederer,dc=fr"
    add_base(server, dn6)
    dn7 = "ou=Apporteurs,ou=Simax Gestion,dc=roederer,dc=fr"
    add_base(server, dn7)

    a = 0
    prGreen("CREATION DES GROUPES ENTREPRISES EN COURS...")
    time.sleep(3)
    for row_entreprises in records_Entreprises:
        if (row_entreprises['GESTIONNAIRE'] == 'ROEDERER'):
            dn = "ou={},ou=Entreprises,ou=Roederer,dc=roederer,dc=fr".format(str(row_entreprises['LID']))
            add_group(server, row_entreprises, dn)
        elif (row_entreprises['GESTIONNAIRE'] == 'SIMAX'):
            dn = "ou={},ou=Entreprises,ou=Simax Santé,dc=roederer,dc=fr".format(str(row_entreprises['LID']))
            add_group(server, row_entreprises, dn)
        else:
            continue

    prGreen("AJOUTS DES ENTREPRISES DANS LES GROUPES EN COURS...")
    time.sleep(3)
    for row_entreprises in records_Entreprises:
        if (row_entreprises['GESTIONNAIRE'] == 'SIMAX'):
            dn = "LID={},ou={},ou=Entreprises,ou=Simax Santé,dc=roederer,dc=fr".format(str(row_entreprises['LID']),
                                                                                       str(row_entreprises['LID']))
            add_user(server, row_entreprises, dn)
        elif (row_entreprises['GESTIONNAIRE'] == 'ROEDERER'):
            dn = "LID={},ou={},ou=Entreprises,ou=Roederer,dc=roederer,dc=fr".format(str(row_entreprises['LID']),
                                                                                    str(row_entreprises['LID']))
            add_user(server, row_entreprises, dn)
        else:
            continue
        a = a + 1

    prGreen("ASSURÉS EN COURS...")
    time.sleep(3)
    for row_personnes in records_Personnes:
        if (row_personnes['GESTIONNAIRE'] == 'ROEDERER'):
            dn = "LID={},ou=Assurés,ou=Roederer,dc=roederer,dc=fr".format(str(row_personnes['LID']))
            add_user(server, row_personnes, dn)
        elif (row_personnes['GESTIONNAIRE'] == 'SIMAX'):
            dn = "LID={},ou=Assurés,ou=Simax Santé,dc=roederer,dc=fr".format(str(row_personnes['LID']))
            add_user(server, row_personnes, dn)
        else:
            continue
        a = a + 1
    prGreen("APPORTEURS EN COURS...")
    time.sleep(3)
    for row_apporteurs in records_Apporteurs:
        dn = "LID={},ou=Apporteurs,ou=Simax Gestion,dc=roederer,dc=fr".format(str(row_apporteurs['LID']))
        add_apporteurs(server, row_apporteurs, dn)
        a = a + 1
    print("Nombre totals d'users (entreprises + assurés + apporteurs", a)


def main():
    try:
        global server
        print("Connexion au LDAP...")
        server = ldap.initialize("ldap://127.0.0.1")  # Modifier l'ip LDAP
        server.simple_bind_s("cn=admin,dc=roederer,dc=fr", "root")
        print("LDAP connected!\nConnexion a la BDD...")
    except:
        print("Error LDAP connection")
    try:
        mydb = mysql.connector.connect(
            host="10.10.45.2",
            user="stagiaire",
            passwd="DjfU78Fj76f65",
            db="RoedererEntreprises"
        )
        print("BDD connected!")
        query(mydb, server)
    except AssertionError as error:
        print(error)


main()
