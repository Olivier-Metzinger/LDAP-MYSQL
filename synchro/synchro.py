# coding=utf-8
import time
import ldap
import logging
import log_mail
import variables
import ldap.modlist
import actions_user
import mysql.connector
from datetime import datetime


def prYellow(skk): print("\033[96m {}\033[00m".format(skk))


def prGreen(skk): print("\033[92m {}\033[00m".format(skk))


def prRed(skk): print("\033[91m {}\033[00m".format(skk))


logging.basicConfig(filename='error_log.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s  --  %(pathname)s  --  %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', )


def query(mydb, server):
    ##REQUETES DU FICHIER DE CONFIG
    EntreprisesQuery = variables.EntreprisesQuery
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(EntreprisesQuery)
    records_Entreprises = cursor.fetchall()

    PersonnesQuery = variables.PersonnesQuery
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(PersonnesQuery)
    records_Personnes = cursor.fetchall()
    data_to_ldap(records_Entreprises, records_Personnes, server)


def data_to_ldap(records_Entreprises, records_Personnes, server):
    # RECUPERE LES ENTREPRISES
    prYellow("ENTREPRISES")
    for row_entreprises in records_Entreprises:
        if (row_entreprises['GESTIONNAIRE'] == "ROEDERER"):
            dn = variables.dn_roed_entr
        elif (row_entreprises['GESTIONNAIRE'] == 'SIMAX'):
            dn = variables.dn_simax_entr
        else:
            continue
            ##VOIR AVEC MORENO##
        existing_entreprises(server, row_entreprises, dn)

    # RECUPERE LES ASSURÉS
    prYellow("ASSURES")
    for row_personnes in records_Personnes:
        if (row_personnes['GESTIONNAIRE'] == "ROEDERER"):
            dn = variables.dn_roed_ass
        elif (row_personnes['GESTIONNAIRE'] == "SIMAX"):
            dn = variables.dn_simax_ass
        else:
            continue
        existing_assures(server, row_personnes, dn)
    # CALL SUR LE LOG MAIL
    log_mail.send_log_mail()


def existing_entreprises(server, row_entreprises, dn):
    group_is_existing = server.search_s(dn, ldap.SCOPE_SUBTREE, "ou={}".format(str(row_entreprises['LID'])))
    # SI LE GROUPE ENTREPRISE N'EXISTE PAS, CRÉER LE GROUPE ET LE USER DEDANS
    if not group_is_existing:
        dn = "ou={},".format(row_entreprises['LID']) + dn
        actions_user.add_group(server, row_entreprises, dn)
        dn = "LID={},".format(row_entreprises['LID']) + dn
        actions_user.add_user(server, row_entreprises, dn)

    # SI LE GROUPE ENTREPRISE EXISTE, JE VERIFIE SI L'USER EXISTE DANS LE GROUPE
    elif group_is_existing:
        dn = "ou={},".format(row_entreprises['LID']) + dn
        user_exist = server.search_s(dn, ldap.SCOPE_SUBTREE, "LID={}".format(str(row_entreprises['LID'])))
        dn = "LID={},".format(row_entreprises['LID']) + dn
        if not user_exist:
            actions_user.add_user(server, row_entreprises, dn)
        elif user_exist:
            actions_user.modify_user(server, row_entreprises, dn)


def existing_assures(server, row_personnes, dn):
    is_existing = server.search_s(dn, ldap.SCOPE_SUBTREE, "LID={}".format(str(row_personnes['LID'])))
    dn = "LID={},".format(str(row_personnes['LID'])) + dn
    # SI L'ASSURÉ N'EXISTE PAS -> AJOUTER DANS LE BON DN
    if not is_existing:
        actions_user.add_user(server, row_personnes, dn)
    # SI IL EXISTE -> MODIFICATION LIST MODIF
    elif is_existing:
        actions_user.modify_user(server, row_personnes, dn)
