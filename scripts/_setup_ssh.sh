#!/usr/bin/expect
set USER root
set IP [lindex $argv 0]
set PASSWD [lindex $argv 1]

spawn telnet $IP

expect "Media_Drive login:"
send "$USER\r"

expect "Password:"
send "$PASSWD\r"

expect "Media_Drive"
send "sed -r -i '1s/(\[a-zA-Z\]:)0/\\1999999/' /etc/shadow\n"

expect "Media_Drive"
send "/etc/init.d/service/sshd start\n"

expect "Media_Drive"
send "exit\n"
interact
