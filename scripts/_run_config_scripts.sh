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
send "/etc/init.d/service/nimbus stop\n"

expect "Media_Drive"
send "python /root/scripts/replace_port_in_nimbus_binary.py\n"

expect "Media_Drive"
send "/etc/init.d/service/nimbus start\n"

expect "Media_Drive"
send "exit\n";
interact

