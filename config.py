#!/usr/bin/python


import ldap
import ldap.modlist

modlist = {
    "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"],
    "uid": ["moreno"],
    "sn": ["cosani"],
    "givenName": ["Moreno"],
    "cn": ["Moreno COSANI"],  ##MODIFIER LES STRINGS COMME BON VOUS SEMBLE
    "displayName": ["Moreno Cosani"],
    "userPassword": ["root"],
    "uidNumber": ["5000"],
    "gidNumber": ["10000"],
    "loginShell": ["/bin/bash"],
    "homeDirectory": ["/home/moreno"]
}

########## ajouter user ##########

def add_user(load):
    global modlist

    dn = "uid=moreno,ou=Personnes,dc=roederer,dc=fr"
    load.add_s(dn, ldap.modlist.addModlist(modlist))



########## modifier user ##########

def modif_user(load):
    global modlist

    dn = "uid=moreno,ou=Personnes,dc=roederer,dc=fr"
    old_value = {"userPassword": ["VIEUX MDP"]}
    new_value = {"userPassword": ["ANCIEN MDP"]}

    modlist = ldap.modlist.modifyModlist(old_value, new_value)
    load.modify_s(dn, modlist)



def main():
    try:
        load = ldap.initialize("ldap://127.0.0.1")
        load.simple_bind_s("cn=admin,dc=roederer,dc=fr", "root")                             #utilisation du compte admin pour effectuer les modifs
        add_user(load)                                                                            #MODIFIER L'APPEL FONCTION POUR CHOISIR LA DEMARCHE A EFFECTUER
    except ldap.LDAPError as e:
        print (e)


main()