from nessrest import ness6rest

# connect to Nessus
scan = ness6rest.Scanner(url="https://localhost:8834", login="sagars", password="mollygeotech07", insecure=True)
# Specify a scan
scan.policy_set(name="sample_template")
scan.scan_add(targets="190.249.221.139, ")
scan.scan_run()