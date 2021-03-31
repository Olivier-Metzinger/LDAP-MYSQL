# coding=utf-8
from datetime import datetime

####DATE SYNCHRO####
date_synchro = datetime(2019, 5, 2, 10, 16, 4)  # Y, M, D, h, m, s

####CONFIG LDAP####
IP_ldap = "ldap://127.0.0.1"
CN_ldap = "cn=admin,dc=roed,dc=fr"
MDP_ldap = "root"

####CONFIG BDD####
DB_host = "IP"
DB_user = "stagiaire"
DB_passwd = "PASS"
DB_DB = "RoedEntreprises"

####REQUETES####

####STRUCTURE LDAP####
##ROED##
dn_roed = "ou=roed,dc=roed,dc=fr"
dn_roed_ass = "ou=Assurés,ou=Roed,dc=roed,dc=fr"
dn_roed_entr = "ou=Entreprises,ou=Roed,dc=roed,dc=fr"


##SIM##
dn_simax = "ou=Sim Santé,dc=roed,dc=fr"  # AJOUT STRUCTURE DE L'ARBRE
dn_simax_ass = "ou=Assurés,ou=Sim Santé,dc=roed,dc=fr"
dn_simax_entr = "ou=Entreprises,ou=Sim Santé,dc=roed,dc=fr"


##SIM##
dn_simax_gestion = "ou=Sim,dc=roed,dc=fr"
dn_simax_gestion_app = "ou=Apporteurs,ou=Sim,dc=roed,dc=fr"

####CONFIG MAIL LOG####
SUBJECT_mail = 'ERROR SYNC LDAP'
FROM_mail = 'mail'
TO_mail = 'mail'
SMTP = 'IP'
