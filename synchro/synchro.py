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

date_synchro = datetime(2019, 5, 2, 10, 16, 4)  # Y, M, D, h, m, s


def query(mydb, server):
    EntreprisesQuery = "SELECT s2.EUID, s2.UPDATEDATE, s1.LID, s1.GESTIONNAIRE, s1.ISACTIVE, s1.DTFIN, s1.PASSWORD, s1.RAISONSOCIALE AS NAME FROM RoedererEntreprises.SBYN_SYSTEMSBR s2 INNER JOIN RoedererEntreprises.SBYN_ENTERPRISE s3 ON s2.EUID = s3.EUID INNER JOIN RoedererEntreprises.SBYN_ENTERPRISE_DETAIL s1 ON s1.LID = s3.LID AND s1.SYSTEMCODE = s3.SYSTEMCODE WHERE s1.SYSTEMCODE = 'AS400' AND s2.UPDATEDATE >= '{}' ".format(
        date_synchro)
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(EntreprisesQuery)
    records_Entreprises = cursor.fetchall()

    PersonnesQuery = "SELECT s2.EUID, s2.UPDATEDATE, s1.LID, s1.GESTIONNAIRE, s1.ISACTIVE, s1.DTFIN, s1.PASSWORD, s1.NOM AS NAME FROM RoedererPersonnes.SBYN_SYSTEMSBR s2 INNER JOIN RoedererPersonnes.SBYN_ENTERPRISE s3 ON s2.EUID = s3.EUID INNER JOIN RoedererPersonnes.SBYN_ENTERPRISE_DETAIL s1 ON s1.LID = s3.LID AND s1.SYSTEMCODE = s3.SYSTEMCODE WHERE s1.SYSTEMCODE = 'AS400' AND s2.UPDATEDATE >= '{}'".format(
        date_synchro)
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(PersonnesQuery)
    records_Personnes = cursor.fetchall()
    data_to_ldap(records_Entreprises, records_Personnes, server)


def data_to_ldap(records_Entreprises, records_Personnes, server):
    prYellow("ENTREPRISES")
    for row_entreprises in records_Entreprises:
        if (row_entreprises['GESTIONNAIRE'] == "ROEDERER"):
            dn = "LID={},ou={},ou=Entreprises,ou=Roederer,dc=roederer,dc=fr".format(str(row_entreprises['LID']),
                                                                                    str(row_entreprises['LID']))
        elif (row_entreprises['GESTIONNAIRE'] == 'SIMAX'):
            dn = "LID={},ou={},ou=Entreprises,ou=Simax Santé,dc=roederer,dc=fr".format(str(row_entreprises['LID']),
                                                                                       str(row_entreprises['LID']))
        else:
            continue
        existing_entreprises(server, row_entreprises, dn)

    prYellow("ASSURES")
    for row_personnes in records_Personnes:
        if (row_personnes['GESTIONNAIRE'] == "ROEDERER"):
            dn = "LID={},ou=Assurés,ou=Roederer,dc=roederer,dc=fr".format(str(row_personnes['LID']))
        elif (row_personnes['GESTIONNAIRE'] == "SIMAX"):
            dn = "LID={},ou=Assurés,ou=Simax Santé,dc=roederer,dc=fr".format(str(row_personnes['LID']))
        else:
            continue
        existing_assures(server, row_personnes, dn)
    log_mail.send_log_mail()


def existing_entreprises(server, row_entreprises, dn):
    if (row_entreprises['GESTIONNAIRE'] == 'SIMAX'):
        dn = "ou=Entreprises,ou=Simax Santé,dc=roederer,dc=fr"
    elif (row_entreprises['GESTIONNAIRE'] == 'ROEDERER'):
        dn = "ou=Entreprises,ou=Roederer,dc=roederer,dc=fr"
    is_existing = server.search_s(dn, ldap.SCOPE_SUBTREE, "ou={}".format(str(row_entreprises['LID'])))
    if (is_existing == []):
        dn = "ou={},".format(row_entreprises['LID']) + dn
        actions_user.add_group(server, row_entreprises, dn)
        dn = "LID={},".format(row_entreprises['LID']) + dn
        actions_user.add_user(server, row_entreprises, dn)
    elif (is_existing != []):
        dn = "ou={},".format(row_entreprises['LID']) + dn
        user_exist = server.search_s(dn, ldap.SCOPE_SUBTREE, "LID={}".format(str(row_entreprises['LID'])))
        if (user_exist == []):
            dn = "LID={},".format(row_entreprises['LID']) + dn
            actions_user.add_user(server, row_entreprises, dn)
        elif (user_exist != []):
            dn = "LID={},".format(row_entreprises['LID']) + dn
            actions_user.modify_user(server, row_entreprises, dn)
    else:
        var = LDAPError, e
        print(var)


def existing_assures(server, row_personnes, dn):
    if (row_personnes['GESTIONNAIRE'] == 'SIMAX'):
        dn = "ou=Assurés,ou=Simax Santé,dc=roederer,dc=fr"
    elif (row_personnes['GESTIONNAIRE'] == 'ROEDERER'):
        dn = "ou=Assurés,ou=Roederer,dc=roederer,dc=fr"
    is_existing = server.search_s(dn, ldap.SCOPE_SUBTREE, "LID={}".format(str(row_personnes['LID'])))
    dn = "LID={},".format(str(row_personnes['LID'])) + dn
    if (is_existing == []):
        actions_user.add_user(server, row_personnes, dn)
    else:
        actions_user.modify_user(server, row_personnes, dn)
