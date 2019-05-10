#!/usr/bin/python
# coding=utf-8

import ldap
import ldap.modlist
import mysql.connector
from datetime import datetime
import time
import actions_user


def prGreen(skk): print("\033[92m {}\033[00m".format(skk))


def prYellow(skk): print("\033[96m {}\033[00m".format(skk))


def prRed(skk): print("\033[91m {}\033[00m".format(skk))


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


def add_structure():
    prGreen("CRÉATION DE L'ARBRE LDAP...")
    time.sleep(3)
    dn = "ou=Roederer,dc=roederer,dc=fr"
    actions_user.add_base(server, dn)
    dn1 = "ou=Assurés,ou=Roederer,dc=roederer,dc=fr"
    actions_user.add_base(server, dn1)
    dn2 = "ou=Entreprises,ou=Roederer,dc=roederer,dc=fr"
    actions_user.add_base(server, dn2)

    dn3 = "ou=Simax Santé,dc=roederer,dc=fr"
    actions_user.add_base(server, dn3)
    dn4 = "ou=Assurés,ou=Simax Santé,dc=roederer,dc=fr"
    actions_user.add_base(server, dn4)
    dn5 = "ou=Entreprises,ou=Simax Santé,dc=roederer,dc=fr"
    actions_user.add_base(server, dn5)

    dn6 = "ou=Simax Gestion,dc=roederer,dc=fr"
    actions_user.add_base(server, dn6)
    dn7 = "ou=Apporteurs,ou=Simax Gestion,dc=roederer,dc=fr"
    actions_user.add_base(server, dn7)


def data_to_ldap(records_Entreprises, records_Personnes, records_Apporteurs, server):
    add_structure()
    a = 0
    prGreen("CREATION DES GROUPES ENTREPRISES EN COURS...")
    time.sleep(3)
    for row_entreprises in records_Entreprises:
        if (row_entreprises['GESTIONNAIRE'] == 'ROEDERER'):
            dn = "ou={},ou=Entreprises,ou=Roederer,dc=roederer,dc=fr".format(str(row_entreprises['LID']))
            actions_user.add_group(server, row_entreprises, dn)
        elif (row_entreprises['GESTIONNAIRE'] == 'SIMAX'):
            dn = "ou={},ou=Entreprises,ou=Simax Santé,dc=roederer,dc=fr".format(str(row_entreprises['LID']))
            actions_user.add_group(server, row_entreprises, dn)
        else:
            continue

    prGreen("AJOUTS DES ENTREPRISES DANS LES GROUPES EN COURS...")
    time.sleep(3)
    for row_entreprises in records_Entreprises:
        if (row_entreprises['GESTIONNAIRE'] == 'SIMAX'):
            dn = "LID={},ou={},ou=Entreprises,ou=Simax Santé,dc=roederer,dc=fr".format(str(row_entreprises['LID']),
                                                                                       str(row_entreprises['LID']))
            actions_user.add_user(server, row_entreprises, dn)
        elif (row_entreprises['GESTIONNAIRE'] == 'ROEDERER'):
            dn = "LID={},ou={},ou=Entreprises,ou=Roederer,dc=roederer,dc=fr".format(str(row_entreprises['LID']),
                                                                                    str(row_entreprises['LID']))
            actions_user.add_user(server, row_entreprises, dn)
        else:
            continue
        a = a + 1

    prGreen("ASSURÉS EN COURS...")
    time.sleep(3)
    for row_personnes in records_Personnes:
        if (row_personnes['GESTIONNAIRE'] == 'ROEDERER'):
            dn = "LID={},ou=Assurés,ou=Roederer,dc=roederer,dc=fr".format(str(row_personnes['LID']))
            actions_user.add_user(server, row_personnes, dn)
        elif (row_personnes['GESTIONNAIRE'] == 'SIMAX'):
            dn = "LID={},ou=Assurés,ou=Simax Santé,dc=roederer,dc=fr".format(str(row_personnes['LID']))
            actions_user.add_user(server, row_personnes, dn)
        else:
            continue
        a = a + 1
    prGreen("APPORTEURS EN COURS...")
    time.sleep(3)
    for row_apporteurs in records_Apporteurs:
        dn = "LID={},ou=Apporteurs,ou=Simax Gestion,dc=roederer,dc=fr".format(str(row_apporteurs['LID']))
        actions_user.add_apporteurs(server, row_apporteurs, dn)
        a = a + 1
    prYellow("Nombre totals d'users (entreprises + personnes + apporteurs {}".format(a))


def main():
    prRed(
        "Ce script va créer les branches ROEDERER, SIMAX SANTÉ, SIMAX GESTION ainsi que leurs sous catégories Entreprises "
        "et Assurés.\n\nCelui-ci va importer les données du MDM vers les groupes correspondants\n\nAppuyez sur 'o' pour lancer le script...")
    while 1:
        key = raw_input("")
        if (key == 'o'):
            break
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
