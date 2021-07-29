import dns.resolver, re
URL = "meraki.com"


DNS_SERVERS = {
    'Google': ['8.8.8.8', '8.8.4.4'],
    'Umbrella': ['208.67.222.222', '208.67.220.220'],
    'Cloud Flare': ['1.0.0.1', '1.1.1.1'],
    'Verisign': ['64.6.64.6', '64.6.65.6']
}

if __name__ == "__main__":
    my_resolver = dns.resolver.Resolver()

    for server in DNS_SERVERS:

        #print(f"Testing with {server} DNS Servers...")
        my_resolver.nameservers = DNS_SERVERS[server]

        ip_addresses = my_resolver.resolve(URL, 'A')
        #print('Result is', end=' ')
        #for ipval in result:
        #    print(ipval.to_text(), end=' ')

        #print('')

        #print('Testing reverse lookups...')
        for ip_address in ip_addresses:
            #print (f"Trying: {ipval}.", end=' ')
            try:
                reverse_lookup = my_resolver.resolve_address(ip_address.to_text())[0].to_text()[:-1]
                #print (f"Result is {result}")
                if reverse_lookup != URL:
                    #print(f"URL Not matching: {result} =/= {URL}")
                    print(f"{server} DNS, {ip_address}: FAIL - URL Mismatch")
                else:
                    print(f"{server} DNS: {ip_address}: PASS")
            except:
                print(f"{server} DNS: {ip_address}: FAIL - exception occured")



        print('')
