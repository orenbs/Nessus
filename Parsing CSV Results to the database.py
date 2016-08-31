# The purpose of this script is to take the generated CSV files and parse them into the database.
# Attributes which need to be parsed: Plugin ID, CVE, CVSS, Risk, Host, Protocol, Port, Name, Synopsis, Description, Solution, See Also, Plugin Output
import csv
import pymysql
import re

# def db_connect():
    # return pymysql.connect(host="10.128.50.165", port=8080, user="sagars", passwd="lollol123", db="shodan_sample_data",charset='utf8', autocommit=True)


def db_connect():
    return pymysql.connect(host="10.128.227.7", port=3306, user="sagars", passwd="lollol123", db="scada_shodan_testing",charset='utf8', autocommit=True)


# Function to remove special characters and camel case
def rmvSpecialCharsandCamelCase(str):
    cleanedtext =  str.translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+'"})
    # cleanedtext = cleanedtext.lower()
    # cleanCamelCase = re.sub("([a-z])([A-Z])","\g<1> \g<2>", cleanedtext)
    return re.sub(' +',' ', cleanedtext)

# set this variable to be the last results set number
results_set_end= 80
cur = db_connect().cursor()

# First, read from the CSV files.
# Second, iterate through the CSV file and store each value into a variable
# Finally, take the stored variables and insert them into the database

failed_inserts = []
i = 0
while i<= results_set_end:
    with open('Results_set_{0}.csv'.format(i), 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pluginID = row['Plugin ID']
            cve = row['CVE']
            cvss = row['CVSS']
            risk = row['Risk']
            host = row['Host']
            protocol = row['Protocol']
            port = row['Port']
            namee = row['Name'].replace("'","")
            synopsis = row['Synopsis'].replace("'","")
            description = row['Description'].replace("'","")
            solution = row['Solution'].replace("'","")
            seealso = row['See Also'].replace("'","")
            pluginoutput = row['Plugin Output'].replace("'","")

            string = """INSERT INTO scada_shodan_testing.nessus_scada_scan_results
                (pluginID, cve, cvss, risk, host, protocol, port, namee, synopsis, description, solution, seealso, pluginoutput)
               VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s');""" % \
                     (pluginID, cve, cvss, risk, host, protocol, port, namee, synopsis, description, solution, seealso, pluginoutput)
            try:
                cur.execute(string)
                print ("Successful insert")
            except:
                print ("Failed insert!")
                print (string)
                failed_inserts.append(string)
    i+=1

print ("There were", len(failed_inserts), "failed inserts")
print (failed_inserts)