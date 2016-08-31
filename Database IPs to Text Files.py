# The purpose of this script is to take all DISTINCT IP addresses from the database with a confidence level of .99
# and output them as text files. Because of the limitations of Nessus, there will be 16 IPs which are outputtted to each file

import pymysql
# Connect to the database shodan_sample_data.shodan_classified_scada

# def db_connect():
#     return pymysql.connect(host="10.128.50.165", port=8080, user="sagars", passwd="lollol123", db="shodan_sample_data",charset='utf8', autocommit=True)


def db_connect():
    return pymysql.connect(host="10.128.227.7", port=3306, user="sagars", passwd="lollol123", db="scada_shodan_testing",charset='utf8', autocommit=True)

# pull the distinct IP addresses from the database, store in a list

cur = db_connect().cursor()
# cur.execute("select distinct(ip_str) from shodan_classified_scada  where conf >= .99")
cur.execute("select distinct(ip_str) from known_scada_vendors")

row = cur.fetchone()
ip_list = [row[0] for row in cur]
print (len(ip_list))

batch_number = 0
ip_list_to_append = []
while len(ip_list)>0:
    ip_list_to_append.append(ip_list.pop())
    if len(ip_list_to_append) == 16:
        o = open("Batch Number {0}.txt".format(batch_number),'w')
        for ip in ip_list_to_append:
            o.write(ip + ", ")
        print("Batch Number ", '%s' % batch_number, ' written successfully!')
        ip_list_to_append = []
        batch_number +=1

print (len(ip_list_to_append))
o = open("Batch Number {0}.txt".format(batch_number), 'w')
for ip in ip_list_to_append:
    o.write(ip + ", ")
print("Batch Number ", '%s' % batch_number, ' written successfully!')
