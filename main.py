#!/usr/bin/python

import query
import ldap
import ldap.modlist
import mysql.connector
import time

def main():
    try:
        global load
        print("Connexion au LDAP...")
        time.sleep(1)
        load = ldap.initialize("ldap://127.0.0.1")                      #Modifier l'ip LDAP
        load.simple_bind_s("cn=admin,dc=roederer,dc=fr","root")
        print("LDAP connected!\nConnexion a la BDD...")
        time.sleep(1)
    except ldap.LDAPError as error:
        print(error)
    try:
        mydb = mysql.connector.connect(
            host="10.10.45.2",
            user="stagiaire",
            passwd="DjfU78Fj76f65",
            db="RoedererEntreprises"
        )
        print(load)
        print("BDD connected!", mydb)
        query.query_up(mydb,load)
    except AssertionError as error:
        print(error)

main()