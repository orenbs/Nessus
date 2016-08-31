# The purpose of this script is to take a set of text files
# Read each one, pull out all of the ip addresses, store them in a variable and start a scan for that specific text file IP addresses

from nessrest import ness6rest

batch_start_number = 0
batch_end_number = 80
nessus_policy_name = "Device Discovery Test"

while batch_start_number <= batch_end_number:
    o = open("Batch Number {0}.txt".format(batch_start_number), 'r')
    targets_list = o.read()
    print ("Processing Batch Number" , '%s' % batch_start_number)
    o.close()
    # connect to Nessus
    # scan = ness6rest.Scanner(url="https://localhost:8834", login="sagars", password="mollygeotech07", insecure=True)
    scan = ness6rest.Scanner(url="https://52.36.138.116:8834", login="sagars", password="mollygeotech07", insecure=True)
    # Specify a scan
    scan.policy_set(name=nessus_policy_name)
    scan.scan_add(targets=targets_list)
    scan.scan_run()
    batch_start_number +=1