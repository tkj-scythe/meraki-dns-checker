import dns.resolver
URL = 'meraki.com'


DNS_SERVERS = {
    'Google': ['8.8.8.8', '8.8.4.4'],
    'Umbrella': ['208.67.222.222', '208.67.220.220'],
    'Cloud Flare': ['1.0.0.1', '1.1.1.1'],
    'Verisign': ['64.6.64.6', '64.6.65.6']
}

if __name__ == "__main__":
    my_resolver = dns.resolver.Resolver()

    for server in DNS_SERVERS:

        print(f"Testing with {server} DNS Servers...")
        my_resolver.nameservers = DNS_SERVERS[server]

        result = my_resolver.resolve(URL, 'A')
        print('Result is', end=' ')
        for ipval in result:
            print(ipval.to_text(), end=' ')

        print('')

        print('Testing reverse lookups...')
        for ipval in result:
            print (f"Trying: {ipval}")
            try:
                if my_resolver.resolve_address(ipval.to_text())[0] != 'URL':
                    print(f"URL Not matching: {my_resolver.resolve_address(ipval.to_text())[0]}")
            except:
                print("DNS Reverse Lookup Exception Occured")



        print('')
