# The purpose of this script is to identify the geographical information for the vulnerable devices identified by Nessus
# Main Logic: Connect to database, store all IP's, call API, parse response, store into database

import pymysql
import json
import urllib.request

# connect to the database, store all of the IP addresses into a list for further processing
def db_connect():
    return pymysql.connect(host="10.128.50.165", port=8080, user="sagars", passwd="lollol123", db="shodan_sample_data",charset='utf8', autocommit=True)

# retrieve all of the IP addresses and store in a list
cur = db_connect().cursor()

cur.execute("select distinct(host) from nessus_scan_results1 where ID > 5212 order by ID;")
results = cur.fetchall()
iplist = [row[0] for row in results]


# Iterate through the IP list, call out to the API, parse out the results, store into variables
# May need to have a time.sleep(30-60) function here make sure not to overload the API

failed_inserts = []

for ip in iplist:
    try:
        http_request = ('http://api.eurekapi.com/iplocation/v1.8/locateip?key=SAKS5X965R54683D3G2Z&ip={}&format=JSON'.format(ip))
        response = urllib.request.urlopen(http_request)
        json_string = response.read().decode('utf-8')
        json_data = json.loads(json_string)

        ip_address = json_data['ip_address']
        continent_code = json_data['geolocation_data']['continent_code']
        continent_name = json_data['geolocation_data']['continent_name']
        country_name = json_data['geolocation_data']['country_name']
        region_code = json_data['geolocation_data']['region_code']
        region_name = json_data['geolocation_data']['region_name']
        city = json_data['geolocation_data']['city']
        postal_code = json_data['geolocation_data']['postal_code']
        metro_code = json_data['geolocation_data']['metro_code']
        area_code = json_data['geolocation_data']['area_code']
        latitude = json_data['geolocation_data']['latitude']
        longitude = json_data['geolocation_data']['longitude']
        isp = json_data['geolocation_data']['isp']
        organization = json_data['geolocation_data']['organization']

        # Insert the variables into the database. Be sure to have file logging for errors.
        string = """INSERT INTO shodan_sample_data.nessus_scan_results_geoip
                     (ip_address, continent_code, continent_name, country_name, region_code, region_name, city, postal_code, metro_code, area_code, latitude, longitude, isp, organization)
                    VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s');""" % \
                 (ip_address, continent_code, continent_name, country_name, region_code, region_name, city, postal_code, metro_code, area_code, latitude, longitude, isp, organization)
        try:
            cur.execute(string)
            print ("Successful Insert!")
        except:
            failed_inserts.append(string)
            print ("Failed Insert!")
    except:
        pass
print (failed_inserts)