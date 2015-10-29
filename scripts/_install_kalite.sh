#!/usr/bin/expect
set timeout 20
set HOST 192.168.11.1
set USER root
set PASSWD [lindex $argv 0]

spawn telnet $HOST


expect "Media_Drive login:"
send "$USER\r"

expect "Password:"
send "$PASSWD\r"

expect "Media_Drive"
send "cd /mnt/storage/\n"

expect "Media_Drive"
send "rm -r ka-lite\n"

expect "Media_Drive"
send "mkdir ka-lite\n"

expect "Media_Drive"
send "cd ka-lite\n"

expect "Media_Drive"
send "unzip ../ka-lite.zip\n"

expect "Media_Drive"
send "python setup.py develop\n"

expect "Media_Drive"
send "sed -i '/django.test.client/ s/^/#/' python-packages/fle_utils/internet/webcache.py\n"

expect "Media_Drive"
send "sed -i '/django.test.signals/ s/^/#/' python-packages/django/contrib/auth/hashers.py\n"

expect "Media_Drive"
send "sed -i '/@receiver(setting_changed)/ s/^/#/' python-packages/django/contrib/auth/hashers.py\n"

expect "Media_Drive"
send "touch .KALITE_SOURCE_DIR\n"

expect "Media_Drive"
send "PYTHONPATH=/mnt/storage/ka-lite/dist-packages python kalitectl.py start\n"

expect "Media_Drive"
send "exit\n";
interact

