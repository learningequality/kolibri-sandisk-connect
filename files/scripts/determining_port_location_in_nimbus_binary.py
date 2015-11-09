"""
This code was used to determine where the port specification was in the nimbus binary, so it could be replaced.
It should not be necessary to run this code again, but it's here in case we need to do something similar again.
"""

import subprocess, urllib2, time, sys

locations = []

# we had to temporarily rename /nimbus/nimbus to /nimbus/nimbus_backup to keep it from auto-restarting
with open("/nimbus/nimbus_backup") as f:
    data = f.read()

for i in range(len(data)):
    if ord(data[i])==80:
        locations.append(i)

print "NUMLOCS", len(locations)

for i in locations:
    data_copy = [ch for ch in data]
    data_copy[i] = chr(82)
    data_mod = "".join(data_copy)
    ex_name = "/nimbus/nimbus_test%d" % i
    with open(ex_name, "w") as f:
        f.write(data_mod)
    print "Replacing at CHAR %d:" % i,
    subprocess.Popen(["/bin/chmod", "+x", ex_name], stdout=subprocess.PIPE).wait()
    proc = subprocess.Popen(ex_name, stdout=subprocess.PIPE)
    proc.wait()
    results = proc.communicate()[0]
    for q in range(20):
        time.sleep(0.1)
        try:
            assert "Media Drive" in urllib2.urlopen("http://192.168.11.1:80/").read()
            print "NORMAL"
            break
        except:
            try:
                assert "Media Drive" in urllib2.urlopen("http://192.168.11.1:82/").read()
                print "MAGIC"
                sys.exit()
            except SystemExit:
                sys.exit()
            except:
                print "BAD"


    time.sleep(0.5)

    # proc.terminate()
    subprocess.Popen(["/usr/bin/killall", ex_name], stderr=subprocess.PIPE).communicate()
    while ex_name in subprocess.Popen(["/bin/ps", "aux"], stdout=subprocess.PIPE).communicate()[0]:
        print ".",
        time.sleep(0.1)
    print "[DONE]"
