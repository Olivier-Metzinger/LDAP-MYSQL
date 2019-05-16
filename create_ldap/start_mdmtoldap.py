#!/usr/bin/python
# coding=utf-8

from datetime import datetime
import mysql.connector
import actions_user
import ldap.modlist
import variables
import ldap
import time


def prGreen(skk): print("\033[92m {}\033[00m".format(skk))


def prYellow(skk): print("\033[96m {}\033[00m".format(skk))  # Fonctions pour print en couleur


def prRed(skk): print("\033[91m {}\033[00m".format(skk))


def query(mydb, server):
    # REQUÊTES ENTREPRISES, ASSURÉS, APPORTEURS (Fichier config)
    EntreprisesQuery = variables.entreprises_query
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(EntreprisesQuery)
    records_Entreprises = cursor.fetchall()

    PersonnesQuery = variables.personnes_query
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(PersonnesQuery)
    records_Personnes = cursor.fetchall()

    ApporteursQuery = variables.apporteurs_query
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(ApporteursQuery)
    records_Apporteurs = cursor.fetchall()

    add_structure(records_Entreprises, records_Personnes, records_Apporteurs, server)


def add_structure(records_Entreprises, records_Personnes, records_Apporteurs, server):
    prGreen("CRÉATION DE L'ARBRE LDAP...")
    time.sleep(3)
    # STRUCTURE ROEDERER
    actions_user.add_base(server, variables.dn_roed)
    actions_user.add_base(server, variables.dn_roed_ass)
    actions_user.add_base(server, variables.dn_roed_entr)
    # STRUCTURE SIMAX SANTÉ
    actions_user.add_base(server, variables.dn_simax)
    actions_user.add_base(server, variables.dn_simax_ass)  ##CREATION DE BASE DE L'ARBRE (VARIABLES.PY)
    actions_user.add_base(server, variables.dn_simax_entr)
    # STRUCTURE SIMAX GESTION
    actions_user.add_base(server, variables.dn_simax_gestion)
    actions_user.add_base(server, variables.dn_simax_gestion_app)
    data_to_ldap(records_Entreprises, records_Personnes, records_Apporteurs, server)


def data_to_ldap(records_Entreprises, records_Personnes, records_Apporteurs, server):
    compteur_ajout = 0

    ##GROUPE ENTREPRISES##
    prGreen("CREATION DES GROUPES ENTREPRISES EN COURS...")
    time.sleep(3)
    for row_entreprises in records_Entreprises:
        if (row_entreprises['GESTIONNAIRE'] == 'ROEDERER'):
            dn = "ou={},".format(
                str(row_entreprises['LID'])) + variables.dn_roed_entr
            actions_user.add_group(server, row_entreprises, dn)

        elif (row_entreprises['GESTIONNAIRE'] == 'SIMAX'):
            dn = "ou={},".format(
                str(row_entreprises['LID'])) + variables.dn_simax_entr
            actions_user.add_group(server, row_entreprises, dn)

    ##UTILISATEURS DANS LE BON GROUPE ENTREPRISE
    prGreen("AJOUTS DES ENTREPRISES DANS LES GROUPES EN COURS...")
    time.sleep(3)
    for row_entreprises in records_Entreprises:
        if (row_entreprises['GESTIONNAIRE'] == 'SIMAX'):
            dn = "LID={},ou={},".format(str(row_entreprises['LID']),
                                        str(row_entreprises['LID'])) + variables.dn_simax_entr  # CRÉATION DES UTILISATEURS DANS LES BONS GROUPES ENTREPRISES
            actions_user.add_user(server, row_entreprises, dn)
        elif (row_entreprises['GESTIONNAIRE'] == 'ROEDERER'):
            dn = "LID={},ou={},".format(str(row_entreprises['LID']),
                                        str(row_entreprises['LID'])) + variables.dn_roed_entr
            actions_user.add_user(server, row_entreprises, dn)
        else:
            var = LDAPError, e
            print(var)
        compteur_ajout = compteur_ajout + 1

    ##UTILISATEURS ASSURÉS
    prGreen("ASSURÉS EN COURS...")
    time.sleep(3)
    for row_personnes in records_Personnes:
        if (row_personnes['GESTIONNAIRE'] == 'ROEDERER'):
            dn = "LID={},".format(str(row_personnes['LID'])) + variables.dn_roed_ass
            actions_user.add_user(server, row_personnes, dn)  # CRÉATION DES ASSURÉS ROEDERER ET/OU SIMAX
        elif (row_personnes['GESTIONNAIRE'] == 'SIMAX'):
            dn = "LID={},".format(str(row_personnes['LID'])) + variables.dn_simax_ass
            actions_user.add_user(server, row_personnes, dn)
        else:
            var = LDAPError, e
            print(var)
        compteur_ajout = compteur_ajout + 1

    ##UTILISATEURS APPORTEURS
    prGreen("APPORTEURS EN COURS...")
    time.sleep(3)
    for row_apporteurs in records_Apporteurs:
        dn = "LID={},".format(str(row_apporteurs['LID'])) + variables.dn_simax_gestion_app
        actions_user.add_apporteurs(server, row_apporteurs, dn)
        compteur_ajout = compteur_ajout + 1
    prYellow("Nombre total d'utilisateurs (entreprises + personnes + apporteurs {}".format(compteur_ajout))


def main():
    prRed(variables.take_care)
    while 1:
        key = raw_input("")
        if (key == 'o' or key == 'O'):
            break
    try:
        global server
        print("Connexion au LDAP...")
        server = ldap.initialize(variables.IP_ldap)  # CONNEXION LDAP ET BDD (fichier config "variables.py")
        server.simple_bind_s(variables.CN_ldap, variables.MDP_ldap)
        print("LDAP connected!\nConnexion à la BDD...")
    except:
        print("Error LDAP connection")
    try:
        mydb = mysql.connector.connect(
            host=variables.DB_host,
            user=variables.DB_user,
            passwd=variables.DB_passwd,
            db=variables.DB_DB
        )
        print("BDD connected!")
        query(mydb, server)
    except AssertionError as error:
        print(error)


main()
