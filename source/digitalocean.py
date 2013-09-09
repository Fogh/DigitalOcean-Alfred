import json
import urllib2
from alp.settings import Settings
from feedback import Feedback

_DEFAULTHOST = "https://api.digitalocean.com"


def set_APIKey(key):
    Settings().set(apikey=key.strip())
    print "API key changed!"


def get_APIKey():
    return Settings().get("apikey")


def set_clientID(client_id):
    Settings().set(clientID=client_id.strip())
    print "Client ID changed!"


def get_clientID():
    return Settings().get("clientID")


def url(path):
    return _DEFAULTHOST + "/" + path + "?client_id=" + get_clientID() + "&api_key=" + get_APIKey()


def get_data(path):
    req = urllib2.Request(url(path))
    try:
        res = urllib2.urlopen(req)
    except urllib2.URLError:
        print "Can't connect to DigitalOcean"
        raise SystemExit()

    return json.loads(res.read())


def list_droplets():
    data = get_data("droplets")
    fb = Feedback()
    if len(data['droplets']) > 0:
        for droplet in data['droplets']:
            name = droplet['name']
            ip_address = droplet['ip_address']
            #status = droplet['status']
            fb.add_item(name, ip_address, ip_address)
    else:
        fb.add_item("No droplets")
    print fb
