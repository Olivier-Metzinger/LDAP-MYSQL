# coding=utf-8
from datetime import datetime

####DATE SYNCHRO####
date_synchro = datetime(2019, 5, 2, 10, 16, 4)  # Y, M, D, h, m, s

####CONFIG LDAP####
IP_ldap = "ldap://127.0.0.1"
CN_ldap = "cn=admin,dc=roederer,dc=fr"
MDP_ldap = "root"

####CONFIG BDD####
DB_host = "10.10.45.2"
DB_user = "stagiaire"
DB_passwd = "DjfU78Fj76f65"
DB_DB = "RoedererEntreprises"

####REQUETES####
EntreprisesQuery = "SELECT s2.EUID, s2.UPDATEDATE, s1.LID, s1.GESTIONNAIRE, s1.ISACTIVE, s1.DTFIN, s1.PASSWORD, s1.RAISONSOCIALE AS NAME FROM RoedererEntreprises.SBYN_SYSTEMSBR s2 INNER JOIN RoedererEntreprises.SBYN_ENTERPRISE s3 ON s2.EUID = s3.EUID INNER JOIN RoedererEntreprises.SBYN_ENTERPRISE_DETAIL s1 ON s1.LID = s3.LID AND s1.SYSTEMCODE = s3.SYSTEMCODE WHERE s1.SYSTEMCODE = 'AS400' AND s2.UPDATEDATE >= '{}' ".format(date_synchro)
PersonnesQuery = "SELECT s2.EUID, s2.UPDATEDATE, s1.LID, s1.GESTIONNAIRE, s1.ISACTIVE, s1.DTFIN, s1.PASSWORD, s1.NOM AS NAME FROM RoedererPersonnes.SBYN_SYSTEMSBR s2 INNER JOIN RoedererPersonnes.SBYN_ENTERPRISE s3 ON s2.EUID = s3.EUID INNER JOIN RoedererPersonnes.SBYN_ENTERPRISE_DETAIL s1 ON s1.LID = s3.LID AND s1.SYSTEMCODE = s3.SYSTEMCODE WHERE s1.SYSTEMCODE = 'AS400' AND s2.UPDATEDATE >= '{}'".format(date_synchro)

####STRUCTURE LDAP####
##ROEDERER##
dn_roed = "ou=Roederer,dc=roederer,dc=fr"
dn_roed_ass = "ou=Assurés,ou=Roederer,dc=roederer,dc=fr"
dn_roed_entr = "ou=Entreprises,ou=Roederer,dc=roederer,dc=fr"


##SIMAX SANTÉ##
dn_simax = "ou=Simax Santé,dc=roederer,dc=fr"  # AJOUT STRUCTURE DE L'ARBRE
dn_simax_ass = "ou=Assurés,ou=Simax Santé,dc=roederer,dc=fr"
dn_simax_entr = "ou=Entreprises,ou=Simax Santé,dc=roederer,dc=fr"


##SIMAX GESTION##
dn_simax_gestion = "ou=Simax Gestion,dc=roederer,dc=fr"
dn_simax_gestion_app = "ou=Apporteurs,ou=Simax Gestion,dc=roederer,dc=fr"

####CONFIG MAIL LOG####
SUBJECT_mail = 'ERROR SYNC LDAP'
FROM_mail = 'pole-web@roederer.fr'
TO_mail = 'pole-web@roederer.fr'
SMTP = '10.10.44.148'