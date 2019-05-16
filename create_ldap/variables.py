# coding=utf-8


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
entreprises_query = "SELECT s1.LID, s1.GESTIONNAIRE, s1.DTFIN, s1.ISACTIVE, s3.PASS, s1.RAISONSOCIALE AS NOM, s1.SYSTEMCODE, s2.EUID FROM RoedererEntreprises.SBYN_ENTERPRISE_DETAIL s1 INNER JOIN TMP_SITEWEB_USER s3 ON s1.LID = s3.LID INNER JOIN SBYN_ENTERPRISE s2 ON s1.LID = s2.LID AND s1.SYSTEMCODE = s2.SYSTEMCODE WHERE s1.SYSTEMCODE = 'AS400' AND s1.GESTIONNAIRE = 'ROEDERER' OR s1.GESTIONNAIRE = 'SIMAX';"
personnes_query = "SELECT s1.LID, s1.SYSTEMCODE, s1.GESTIONNAIRE, s1.ISACTIVE, s3.PASS, s1.DTFIN, s1.NOM, s2.EUID FROM RoedererPersonnes.SBYN_ENTERPRISE_DETAIL s1 INNER JOIN RoedererEntreprises.TMP_SITEWEB_USER s3 ON s1.LID = s3.LID INNER JOIN RoedererPersonnes.SBYN_ENTERPRISE s2 ON s1.LID = s2.LID AND s1.SYSTEMCODE = s2.SYSTEMCODE WHERE s1.SYSTEMCODE = 'AS400' AND s1.GESTIONNAIRE = 'ROEDERER' OR s1.GESTIONNAIRE = 'SIMAX';"
apporteurs_query = "SELECT ID_USER AS LID, GESTIONNAIRE, PASS, TYPE_USER, LID FROM RoedererEntreprises.TMP_SITEWEB_USER WHERE TYPE_USER = 'app';"


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


##WARNING##
take_care = "Ce script va créer les branches ROEDERER, SIMAX SANTÉ, SIMAX GESTION ainsi que leurs sous catégories Entreprises, Assurés ou apporteur.\n\n" \
            "Celui-ci va importer les données du MDM vers les groupes correspondants.\n\n!! " \
            "ATTENTION !! Ce script utilise des attributs personnalisés, c'est pourquoi il faudra d'abord ajouter votre propre schéma et ses attributs dans votre LDAP\n\n" \
            "Appuyez sur 'o' puis la touche entrée pour lancer le script..."
