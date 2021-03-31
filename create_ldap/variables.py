# coding=utf-8


####CONFIG LDAP####
IP_ldap = "ldap://127.0.0.1"
CN_ldap = "cn=admin,dc=roed,dc=fr"
MDP_ldap = "root"


####CONFIG BDD####
DB_host = "addip"
DB_user = "olivier"
DB_passwd = "DjfU78Fj76f65"
DB_DB = "Roed"



####STRUCTURE LDAP####
##dn_roed##
dn_roed = "ou=roed,dc=roed,dc=fr"
dn_roed_ass = "ou=Assurés,ou=Roed,dc=roed,dc=fr"
dn_roed_entr = "ou=Entreprises,ou=Roed,dc=roed,dc=fr"


##dn_roed ##
dn_simax = "ou=Sim,dc=roed,dc=fr"  # AJOUT STRUCTURE DE L'ARBRE
dn_simax_ass = "ou=Assurés,ou=Sim,dc=roed,dc=fr"
dn_simax_entr = "ou=Entreprises,ou=Sim,dc=roed,dc=fr"


##SIMAX GESTION##
dn_simax_gestion = "ou=Sim,dc=roed,dc=fr"
dn_simax_gestion_app = "ou=Apporteurs,ou=Sim,dc=roed,dc=fr"


##WARNING##
take_care = "Ce script va créer les branches ROED, SIM, SIM ainsi que leurs sous catégories Entreprises, Assurés ou apporteur.\n\n" \
            "Celui-ci va importer les données du MDM vers les groupes correspondants.\n\n!! " \
            "ATTENTION !! Ce script utilise des attributs personnalisés, c'est pourquoi il faudra d'abord ajouter votre propre schéma et ses attributs dans votre LDAP\n\n" \
            "Appuyez sur 'o' puis la touche entrée pour lancer le script..."
