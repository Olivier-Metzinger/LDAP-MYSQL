#!/usr/bin/python
# coding=utf-8

import ldap

def prRed(skk): print("\033[91m {}\033[00m".format(skk))

if __name__ == "__main__":
    #CONFIG
    ldap_server = "ldap://127.0.0.1"
    login = "000000300"
    password= "pass"

    connect = ldap.initialize(ldap_server)
    # DN complet user
    user_dn = "LID="+login+",ou=Assurés,ou=roed,dc=roed,dc=fr"
    # DN de recherche (sans LID user)
    base_dn = "ou=Assurés,ou=Roed,dc=roed,dc=fr"
    # filtre de recherche
    search_filter = "LID="+login
    try:
        # Si l'auth passe, recupère tout le user data
        connect.bind_s(user_dn,password)
        result = connect.search_s(base_dn,ldap.SCOPE_SUBTREE,search_filter)
        # On ferme la connexion
        connect.unbind_s()
        prRed(result)
    except ldap.LDAPError:
        connect.unbind_s()
        print "authentication error"
