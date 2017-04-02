# -*- coding: utf-8 -*-

import subprocess
import socket

import dns.resolver

# TW/JP/KR/HK/SG
DNS_LIB = [
    {
        'name': 'HiNet',
        'country': 'TW',
        'nameservers': ['168.95.1.1', '168.95.192.1', '168.95.192.2']
    },
    {
        'name': 'IIJ',
        'country': 'JP',
        'nameservers': ['210.130.0.1', '210.130.1.1']
    },
    {
        'name': 'WTT',
        'country': 'HK',
        'nameservers': ['202.130.97.65', '202.130.97.66']
    },
    {
        'name': 'SK',
        'country': 'KR',
        'nameservers': ['210.220.163.82', '219.250.36.130']
    },
    {
        'name': 'KT',
        'country': 'KR',
        'nameservers': ['168.126.63.1', '168.126.63.2']
    },
    {
        'name': 'LG',
        'country': 'KR',
        'nameservers': ['164.124.101.2', '203.248.252.2']
    },
    {
        'name': 'Singtel',
        'country': 'SG',
        'nameservers': ['165.21.83.88', '165.21.100.88']
    },
    {
        'name': 'Google DNS',
        'country': 'ANYCAST',
        'nameservers': ['8.8.8.8', '8.8.4.4']
    },
]


DNS_LIB_NAME = {}
for ns in DNS_LIB:
    for nameserver in ns['nameservers']:
        DNS_LIB_NAME[nameserver] = ns['name']

# twitter/google/instagram/youtube
# twitter.com api.twitter.com pbs.twimg.com
# instagram.com api.instagram.com scontent.cdninstagram.com
# http://redirector.c.youtube.com/report_mapping s.ytimg.com
# www.google.com www.gstatic.com apis.google.com www.googleapis.com clients4.google.com

HOSTS = ['twitter.com', 'api.twitter.com', 'pbs.twimg.com',
         'instagram.com', 'api.instagram.com', 'scontent.cdninstagram.com',
         's.ytimg.com', 'www.google.com', 'www.gstatic.com',
         'apis.google.com', 'www.googleapis.com', 'clients4.google.com']

def get_local_resolver():
    local_resolver = dns.resolver.Resolver(configure=True)
    return local_resolver.nameservers


def get_dns_with_resolver(nameserver, names):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [nameserver]
    result = []
    for name in names:
        answers = resolver.query(name, 'a')
        for answer in answers:
            result.append(answer.to_text())
            break
    return result


def fping(domains, times=5):
    cmd = '/usr/bin/fping -q -C %s -B1 -r1 -i10 %s | true' % (times, ' '.join(domains))
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    return output


def main():
    local_dns = get_local_resolver()
    print 'System DNS: %s (%s)' % (local_dns[0], DNS_LIB_NAME.get(local_dns[0]) or 'Unknown')

    hostname = socket.gethostname()
    test_nameservers = []
    for ns in DNS_LIB:
        if ns['country'] == 'ANYCAST':
            test_nameservers.append(ns['nameservers'][0])
        elif ns['country'].lower() in hostname.lower():
            test_nameservers.append(ns['nameservers'][0])

    for nameserver in test_nameservers:
        print '\nTesting with %s (%s):' % (nameserver, DNS_LIB_NAME.get(nameserver) or 'Unknown')
        ips = get_dns_with_resolver(nameserver, HOSTS)
        result = fping(ips)

        for i, line in enumerate(result.splitlines()):
            print '%s\t%s' % (line, HOSTS[i])

if __name__ == '__main__':
    main()
