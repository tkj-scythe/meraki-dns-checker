import dns.resolver
import meraki
import urllib.request

URL = "meraki.com"


DNS_SERVERS = {
    'Google': ['8.8.8.8', '8.8.4.4'],
    'Umbrella': ['208.67.222.222', '208.67.220.220'],
    'Cloud Flare': ['1.0.0.1', '1.1.1.1'],
    'Verisign': ['64.6.64.6', '64.6.65.6'],
    'Google Syndey': ['74.125.18.128']
}

# Either uncomment and set this (not recommended) or export your API to an Environment Variable
# usings export MERAKI_DASHBOARD_API_KEY = xxxx
# MERAKI_DASHBOARD_API_KEY = xxxx

def getWanInterface(external_ip, dashboard):
    organizations = dashboard.organizations.getOrganizations()
    for org in organizations:
        #print(f'--Analyzing organization {org["name"]}:')
        org_id = org['id']
        try:
            appliances = dashboard.appliance.getOrganizationApplianceUplinkStatuses(org_id)
        except meraki.APIError as e:
            print(f'Meraki API error: {e}')
            print(f'status code = {e.status}')
            print(f'reason = {e.reason}')
            print(f'error = {e.message}')
            continue
        except Exception as e:
            print(f'some other error: {e}')
            continue

        else:
            if appliances:
                for appliance in appliances:
                    #print(f' \--Analyzing appliance {appliance["serial"]}:')
                    interfaces = appliance['uplinks']
                    for interface in interfaces:
                        #print(f' | \-Analyzing interface {interface["interface"]} - IP address: {interface["publicIp"]}:')
                        if external_ip == interface["publicIp"]:
                            #print(f' |  \- Matches interface {interface["interface"]} - IP address: {interface["publicIp"]}:')
                            print(f'Network found, Org: {org["name"]}, Appliance: {appliance["serial"]}, Interface: {interface["interface"]}')
                            return (org, appliance, interface)
        print(f'Failed to find interface')
        return None


if __name__ == "__main__":

    #Get external IP address
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    print(f'External IP address is {external_ip}:')

    #Connect to meraki dashboard
    dashboard = meraki.DashboardAPI(print_console=False)

    org, appliance, interface = getWanInterface(external_ip, dashboard)

    current_dns_servers = {interface["primaryDns"] : "Unknown", interface["secondaryDns"]: "Unknown" }

    for server in DNS_SERVERS:
        for current in current_dns_servers:
            if current in DNS_SERVERS[server]:
                current_dns_servers[current] = server
                #print(f'Using {server} DNS Server')



    #Cycle through, orgs, networks and appliances to see if IP addresses match




    my_resolver = dns.resolver.Resolver()
    for server in DNS_SERVERS:

        #print(f"Testing with {server} DNS Servers...")
        my_resolver.nameservers = DNS_SERVERS[server]
        my_resolver.lifetime = 4
        my_resolver.timeout = 2



        try:
            ip_addresses = my_resolver.resolve(URL, 'A')
            for ip_address in ip_addresses:
                #print (f"Trying: {ipval}.", end=' ')
                try:
                    reverse_lookup = my_resolver.resolve_address(ip_address.to_text())[0].to_text()[:-1]
                    #print (f"Result is {result}")
                    if reverse_lookup != URL:
                        #print(f"URL Not matching: {result} =/= {URL}")
                        print(f"{server} DNS, {ip_address}: FAIL - URL Mismatch, returned URL is {reverse_lookup}")
                    else:
                        print(f"{server} DNS: {ip_address}: PASS")
                except Exception as e:
                    print(f"{server} DNS: {ip_address}: FAIL - exception occured: {e.msg}")
        except Exception as e:
            print(f"{server} DNS: {ip_address}: FAIL forward lookup - exception occured: {e.msg}")
        #print('Result is', end=' ')
        #for ipval in result:
        #    print(ipval.to_text(), end=' ')

        #print('')

        #print('Testing reverse lookups...')


        #check existing DNS servers, do they work?
        #check if passing DNS servers == existing DNS Servers
        #check you are running from the same IP Address as meraki networks
        #Update DNS servers
