#!/usr/bin/python


import ldap
import ldap.modlist
import mysql.connector

modlist = {
    "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"],
    "uid": ["ff"],
    "sn": ["cosani"],
    "givenName": ["Moreno"],
    "cn": ["Moreno COSANI"],                                                                ##MODIFIER LES STRINGS COMME BON VOUS SEMBLE (set en global)(class et value)
    "displayName": ["Moreno Cosani"],
    "userPassword": ["root"],
    "uidNumber": ["5000"],
    "gidNumber": ["10000"],
    "loginShell": ["/bin/bash"],
    "homeDirectory": ["/home/moreno"]
}
row = 0
load = 0
mydb = 0

def add_user(row):
    global modlist

    print(row[0])
    dn = "uid={},ou=Personnes,dc=roederer,dc=fr".format(row[0])                                            #MODIFIER LE DN (chemin)
    try:
        load.add_s(dn, ldap.modlist.addModlist(modlist))
        print("Utilisateur added")
    except:
        print("Erreur, verifiez votre dn, et controler que son uid n'existe pas deja")
        return 84

def main():
    try:
        global load
        global row
        load = ldap.initialize("ldap://127.0.0.1")                      #Modifier l'ip LDAP
        load.simple_bind_s("cn=admin,dc=roederer,dc=fr", "root")
        print ("LDAP connected! Connexion a la BDD...")
    except ldap.LDAPError as e:
        print (e)
    try:
        global mydb
        mydb = mysql.connector.connect(
            host="10.10.45.2",
            user="stagiaire",
            passwd="DjfU78Fj76f65"
        )
        print("BDD connected!", mydb)
        sql_select_Query = "SELECT * FROM RoedererEntreprises.SBYN_ENTERPRISE WHERE LID='C0272137'"
        cursor = mydb.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        for row in records:
            print(row[0])
            print(row[1])
            print(row[2])
        print("Total de rows : ", cursor.rowcount)
        add_user(row)
    except:
        print("Erreur BDD (verifiez l'host, le user, ou le passwd...)")


main()