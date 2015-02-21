#!/usr/bin/env python
import requests, datetime, socket, time

# WMD lasted 5:22 under the following regimen, while also connected to the internet on its other adapter
# WMD lasted 32:02 under the following regimen, without being connected to the internet, while connected to 10K Mah Anker battery

start = datetime.datetime.now()

while True:
    try:
        r = requests.get("http://192.168.11.1:8008/", timeout=5)
        print r
        if r.status_code == 200:
            break
    except Exception, e:
        print e
        time.sleep(5)

stop = datetime.datetime.now()

print stop - start