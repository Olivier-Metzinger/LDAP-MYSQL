#!/usr/bin/python


import ldap
import ldap.modlist
import mysql.connector


row = 0
load = 0
mydb = 0
mdm = 0

def add_user(row, a):
    modlist = {
        "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"],
        "uid": ["{}".format(a)],
        "sn": ["{}".format(row[1])],
        "givenName": ["Moreno"],
        "cn": ["Moreno COSANI"],  ##MODIFIER LES STRINGS COMME BON VOUS SEMBLE (set en global)(class et value)
        "displayName": ["Moreno Cosani"],
        "userPassword": ["root"],
        "uidNumber": ["5000"],
        "gidNumber": ["10000"],
        "loginShell": ["/bin/bash"],
        "homeDirectory": ["/home/{}".format(row[1])]
    }
    dn = "uid={},ou=fafa,dc=roederer,dc=fr".format(a)                                            #MODIFIER LE DN (chemin)

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

        global mdm
        mdm = mysql.connector.connect(
            host="10.10.45.2",
            user="stagiaire",
            passwd="DjfU78Fj76f65",
            db="RoedererEntreprises"
        )
        print("BDD connected!", mydb)
        print("MDM connected!", mdm)
        sql_select_Query = "SELECT SBYN_ENTERPRISE.SYSTEMCODE, SBYN_ENTERPRISE.LID, SBYN_ENTERPRISE.EUID, SBYN_ENTREPRISE_DETAIL.GESTIONNAIRE, SBYN_ENTREPRISE_DETAIL.ISACTIVE FROM SBYN_ENTERPRISE LEFT JOIN SBYN_ENTREPRISE_DETAIL  ON SBYN_ENTERPRISE.SYSTEMCODE = SBYN_ENTREPRISE_DETAIL.SYSTEMCODE AND SBYN_ENTERPRISE.LID = SBYN_ENTREPRISE_DETAIL.LID"
        cursor = mdm.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        a=0
        for row in records:
            a = a + 1
            print(row)
            print(a)
    except:
        print("Erreur BDD ou MDM (verifiez l'host, le user, ou le passwd...)")


main()


