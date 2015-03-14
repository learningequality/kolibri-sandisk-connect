#!/usr/bin/expect
set timeout 20
set HOST 192.168.11.1
set USER root
set PASSWD [lindex $argv 0]
set WIPI_IP [lindex $argv 1]

spawn telnet $HOST


expect "Media_Drive login:"
send "$USER\r"

expect "Password:"
send "$PASSWD\r"

expect "Media_Drive"
send "ip addr add $WIPI_IP/24 dev wlan0\n"

expect "Media_Drive"
send "exit\n";
interact

