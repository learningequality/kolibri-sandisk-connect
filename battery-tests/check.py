import requests, datetime, socket

# WMD lasted 5:22 under the following regimen, while also connected to the internet on its other adapter

while True:
    print datetime.datetime.now(), "\t",
    try:
        r = requests.get("http://192.168.11.1:8008/content/IgYUR7aFY-c.mp4", timeout=10)
        print r.status_code,
        r = requests.get("http://192.168.11.1:8008/", timeout=10)
        print r.status_code
    except Exception, e:
        print str(e)

