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
send "mkdir /mnt/storage/.kalite\n"

expect "Media_Drive"
send "rm /root/.kalite 2> /dev/null; ln -s /mnt/storage/.kalite /root/.kalite\n"

expect "Media_Drive"
send "mkdir /mnt/storage/.usrsharekalite\n"

expect "Media_Drive"
send "rm /usr/share/kalite 2> /dev/null; ln -s /mnt/storage/.usrsharekalite /usr/share/kalite\n"

expect "Media_Drive"
send "cd /mnt/storage/\n"

expect "Media_Drive"
send "rm -r ka-lite-static-0.16.0\n"

expect "Media_Drive"
send "tar -zxvf ka-lite-static-0.16.0.tar.gz\n"

expect "Media_Drive"
send "cd ka-lite-static-0.16.0\n"

expect "Media_Drive"
send "python setup.py install\n"

expect "Media_Drive"
send "PYTHONPATH=/mnt/storage/ka-lite-static-0.16.0/dist-packages python kalitectl.py manage unpack_assessment_zip /mnt/storage/khan_assessment.zip\n"

interact

