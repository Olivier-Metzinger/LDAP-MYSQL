#!/usr/bin/python
# coding=utf-8

from log_mail import send_log_mail
import variables
import synchro
import ldap
import logging
import ldap.modlist
import sys
import mysql.connector
import time


def main():
    try:
        global load
        print("Connexion au LDAP...")
        server = ldap.initialize(variables.IP_ldap)
        server.simple_bind_s(variables.CN_ldap, variables.MDP_ldap)
        print("LDAP connected!\nConnexion a la BDD...")
    except:
        logging.error('Error on LDAP connection')
    try:
        mydb = mysql.connector.connect(
            host=variables.DB_host,
            user=variables.DB_user,
            passwd=variables.DB_passwd,
            db=variables.DB_DB
        )
        print("BDD connected!")
    except:
        logging.error('Error on DATABASE connection')
    synchro.query(mydb, server)


main()