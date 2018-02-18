from flask import Flask, render_template, request
import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import locations

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/register", methods=["POST"])
def register():
    if request.form["name"] == "":
        return render_template('failure.html')
    result = get_items(str(request.form["name"]))
    locations.main(result)
    return render_template('Map.html')


def process_json(data, connection):
    js = json.loads(data)
    json.dumps(js, indent=2)
    name = 'location'
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
    return dictionary


def get_items(name):
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    while True:
        acct = name
        if (len(acct) < 1): break
        url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '1'})
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()
        result = process_json(data, connection)
    return result


if __name__ == '__main__':
    app.run(debug=True, port=8080)
