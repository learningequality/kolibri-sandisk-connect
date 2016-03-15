#!/usr/bin/expect
set HOST 192.168.11.1
set USER root
set PASSWD [lindex $argv 0]

spawn telnet $HOST

expect "Media_Drive login:"
send "$USER\r"

expect "Password:"
send "$PASSWD\r"

expect "Media_Drive"
send "sed -r -i '1s/(\[a-zA-Z\]:)0/\\1999999/' /etc/shadow\n"

expect "Media_Drive"
send "/etc/init.d/service/sshd start\n"
