#!/usr/bin/python


import ldap
import ldap.modlist

modlist = {
    "objectClass": ["inetOrgPerson", "posixAccount"],
    "uid": ["NAME"],
    "sn": ["SURNAME"],
    "givenName": ["OLIVIER"],
    "cn": ["OLIVIER MTZG"],                                                                ##MODIFIER LES STRINGS COMME BON VOUS SEMBLE (set en global)(class et value)
    "displayName": ["OLIVIER MTZG"],

    "userPassword": ["root"],
    "uidNumber": ["4000"],
    "gidNumber": ["40000"],
    "loginShell": ["/bin/bash"],
    "homeDirectory": ["/home/moeno"]
}

########## ajouter user ##########

def add_user(load):
    global modlist

    dn = "uid=OLIVIER,ou=People,dc=roed,dc=fr"                                            #MODIFIER LE DN (chemin)
    try:
        load.add_s(dn, ldap.modlist.addModlist(modlist))
        print("Utilisateur added")
    except:
        print("Erreur, verifiez votre dn, et controler que son uid n'existe pas deja")
        return 84


########## modifier user ##########

def modif_user(load):
    global modlist

    dn = "uid=Olivier,ou=People,dc=roed,dc=fr"
    try:
        old_value = {"pwdAccountLockedTime": [""]}                                            #MODIFIER LA CLASS ET TOUJOURS METTRE ANCIENNE VALEUR, PUIS NOUVELLE
        new_value = {"pwdAccountLockedTime": ["000001010000Z"]}
        modlist = ldap.modlist.modifyModlist(old_value, new_value)
        load.modify_s(dn, modlist)
        print("Valeur modifiee")
    except:
        print("Erreur, verifiez votre dn, et controler que l'ancienne valeur est bonne")
        return 84



########## supprimer user (par defaut) ##########

def delete_user(load):
    try:
        dn = "uid=Olivier,ou=Personnes,dc=roed,dc=fr"                                              #MODIFIER LE DN
        load.delete_s(dn)
        print("Supprime avez succes!")
    except:
        print("Erreur, avez-vous entre le bon DN ?")
        return 84


def main():
    try:
        load = ldap.initialize("ldap://127.0.0.1")                                           #Modifier l'ip LDAP
        load.simple_bind_s("cn=admin,dc=roed,dc=fr", "root")                             #utilisation du compte admin pour effectuer les modifs
        add_user(load)                                                                    #MODIFIER L'APPEL FONCTION POUR CHOISIR LA DEMARCHE A EFFECTUER
    except ldap.LDAPError as e:
        print (e)


main()
