#!/usr/bin/env python3
import sys
import requests

# Cloudflare API credentials
email   = ""
api_key = ""
zone_id = ""
domain  = ""

# Cloudflare API endpoint
api_url = "https://api.cloudflare.com/client/v4"
headers = {
    "Content-Type": "application/json",
    "X-Auth-Email": email,
    "X-Auth-Key": api_key
}

# Get current IP address
try:
    local_ipv4 = requests.get('http://ipv4.icanhazip.com').text.strip()
except:
    local_ipv4 = None
try:
    local_ipv6 = requests.get('http://ipv6.icanhazip.com').text.strip()
except:
    local_ipv6 = None
print(f"Current IPv4 address is {local_ipv4}")
print(f"Current IPv6 address is {local_ipv6}")
if local_ipv4 == None and local_ipv6 == None:
    print("Please check network connection!")
    sys.exit(0)

# Get dns_id and IP address of DNS record
params = {"name": domain, "type": "A"}
r = requests.get(f"{api_url}/zones/{zone_id}/dns_records", headers=headers, params=params)
r.raise_for_status()
dns_id_a = r.json()["result"][0]["id"]
dns_ipv4 = r.json()["result"][0]["content"]

params = {"name": domain, "type": "AAAA"}
r = requests.get(f"{api_url}/zones/{zone_id}/dns_records", headers=headers, params=params)
r.raise_for_status()
dns_id_aaaa = r.json()["result"][0]["id"]
dns_ipv6 = r.json()["result"][0]["content"]

if local_ipv4 != None:
    params = {"name": domain, "type": "A"}
    r = requests.get(f"{api_url}/zones/{zone_id}/dns_records", headers=headers, params=params)
    dns_ipv4 = r.json()["result"][0]["content"]
    dns_id = r.json()["result"][0]["id"]
    print(f"DNS record type A is {dns_ipv4}")
    if local_ipv4 != dns_ipv4:
        # Update record type A
        data = {'type': 'A', 'name': domain, 'content': local_ipv4}
        requests.put(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_id}', headers=headers, json=data)
        print("IPv4 record updated!")
    else:
        print("IPv4 address not changed yet!")
if local_ipv6 != None:
    params = {"name": domain, "type": "AAAA"}
    r = requests.get(f"{api_url}/zones/{zone_id}/dns_records", headers=headers, params=params)
    dns_ipv6 = r.json()["result"][0]["content"]
    dns_id = r.json()["result"][0]["id"]
    print(f"DNS record type AAAA is {dns_ipv6}")
    if local_ipv6 != dns_ipv6:
        # Update record type AAAA
        data = {'type': 'AAAA', 'name': domain, 'content': local_ipv6}
        requests.put(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_id}', headers=headers, json=data)
        print("IPv6 record updated!")
    else:
        print("IPv6 address not changed yet!")