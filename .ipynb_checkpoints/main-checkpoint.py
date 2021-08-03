import dns.resolver
URL = "meraki.com"


DNS_SERVERS = {
    'Google': ['8.8.8.8', '8.8.4.4'],
    'Umbrella': ['208.67.222.222', '208.67.220.220'],
    'Cloud Flare': ['1.0.0.1', '1.1.1.1'],
    'Verisign': ['64.6.64.6', '64.6.65.6'],
    'Google Syndey': ['74.125.18.128']
}

if __name__ == "__main__":
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
