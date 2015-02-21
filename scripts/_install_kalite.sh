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
send "cd kalite\n"

# TODO-BLOCKER(jamalex): what should username and password be set to?
expect "Media_Drive"
send "./manage.py setup --noinput -u admin -e test@test.com -p pass -o 'Demo Server' -d 'A Demo Server'"

expect "Media_Drive"
send "exit\n";
interact

