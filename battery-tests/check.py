#!/usr/bin/env python
import requests, datetime, socket

# WMD lasted 5:22 under the following regimen, while also connected to the internet on its other adapter
# WMD lasted 32:02 under the following regimen, without being connected to the internet, while connected to 10K Mah Anker battery

while True:
    result = str(datetime.datetime.now()) + "\t"
    try:
        r = requests.get("http://192.168.11.1:8008/content/IgYUR7aFY-c.mp4", timeout=10)
        result += " " + str(r.status_code)
        r = requests.get("http://192.168.11.1:8008/", timeout=10)
        result += " " + str(r.status_code)
    except Exception, e:
        result += str(e)
    with open("results.txt", "a") as f:
        f.write(result + "\n")
        print result

