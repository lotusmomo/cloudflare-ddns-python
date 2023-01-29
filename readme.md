# A simple Dynamic DNS script

You should change the Cloudflare API credentials first:

```python
# Cloudflare API credentials
email   = "admin@example.com"
api_key = "sdfsdfsdfsfsfsfsfsdfsfgdfghdfhgrtgsfgh"
zone_id = "afsdfgsdgsgsfdgdfsgdfgdgdfgfd"
domain  = "a.example.com"
```

The script supports IPv4 and IPv6, the IP addresses are got from APIs of `icanhazip.com`. You should create records first before running the script, temporary IP address `127.0.0.1` for record type A and `::1` for AAAA works fine. But creating AAAA record for IPv4-only clients is not recommended, so do IPv6-only clients.

And use `crontab -e` to add the crontab:

```
*/5 * * * * /usr/bin/python3 /path/to/script.py 2>&1 >> /path/to/ddns.log
```

Then the script will run every 5 mins.