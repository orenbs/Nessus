# The purpose of this script is to download all of the Nessus CSV files to the local disk.
# Later, this script will be extended to parse the files into the database
# The acceptable file outputs for this script are CSV, DB, HTML, and XML (Nessus)

import nessrest
from nessrest import ness6rest
import sys

sys.path.append('../')
import getpass
user = "sagars"
password = "mollygeotech07"

scan = ness6rest.Scanner(url="https://52.36.138.116:8834",login=user,password=password, insecure=True)
scan.action(action="scans", method="get")

scan_number = 0

for s in scan.res['scans']:
  scan.scan_name = s['name']
  scan.scan_id = s['id']
  csv_nessus = scan.download_scan(export_format='csv')
  fp = open('Results_set_%s.csv'%(scan_number),"w")
  fp.write(csv_nessus)
  fp.close()
  scan_number+=1