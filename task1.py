import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def process_json(data):
    js = json.loads(data)
    json.dumps(js, indent=2)
    name = str(input("What do you want to see? "))
    headers = dict(connection.getheaders())
    print('Remaining', headers['x-rate-limit-remaining'])
    f = open('result.txt', 'w', encoding='utf-8')
    dictionary = {}
    for u in js['users']:
        dictio = {}
        key = u['screen_name']
        if 'status' not in u:
            print('   * No status found')
            continue
        s = u[name]
        dictio[key] = s
        dictionary.update(dictio)
    f.write(str(dictionary))
    f.close()


while True:
    print('')
    acct = input('Enter Twitter Account:')
    if (len(acct) < 1): break
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '20'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    process_json(data)
print("Lock at the result.txt")