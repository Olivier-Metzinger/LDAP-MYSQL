# coding=utf-8
import ldap
import ldap.modlist
import mysql.connector
import datetime


def add_user(load, row, dn):
    date = datetime.datetime.now()
    modlist = {
        "objectClass": ["RoedererClass", "inetOrgPerson"],
        "LID": ["{}".format(row[0])],
        "uid": ["{}".format(row[14])],
        "Actif": ["1"],
        "DateFinActif": ["{}".format(row[3])],
        "DateMajMdp": ["{}".format(date)],
        "userPassword": ["{}".format(row[9])],
        "MdpInitial": ["Non"],
        "cn": ["{}".format(row[6].encode("utf-8"))],
        "sn": ["{}".format(row[6].encode("utf-8"))],
    }
    try:
        load.add_s(dn, ldap.modlist.addModlist(modlist))
        print("Utilisateur added")
    except AssertionError as error:
        print(error)

def query_up(mydb, load):
    sql_select_Query = "SELECT * FROM RoedererEntreprises.SBYN_ENTERPRISE_DETAIL INNER JOIN TMP_SITEWEB_USER ON SBYN_ENTERPRISE_DETAIL.LID = TMP_SITEWEB_USER.LID INNER JOIN SBYN_ENTERPRISE ON SBYN_ENTERPRISE_DETAIL.LID = SBYN_ENTERPRISE.LID AND SBYN_ENTERPRISE_DETAIL.SYSTEMCODE = SBYN_ENTERPRISE.SYSTEMCODE WHERE SBYN_ENTERPRISE_DETAIL.SYSTEMCODE = 'AS400'"
    cursor = mydb.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    for row in records:
        if (row[2] == "ROEDERER"):
            dn = "LID={},ou=Entreprise,ou=Roederer,dc=roederer,dc=fr".format(row[0])  # MODIFIER LE DN (chemin)
        elif (row[2] == "SIMAX"):
            dn = "LID={},ou=Entreprise,ou=Simax Santé,dc=roederer,dc=fr".format(row[0])
        else:
            continue
        add_user(load, row, dn)
    print("Total de rows : ", cursor.rowcount)