#!/bin/sh
HOST='192.168.11.1'
USER='root'

echo "Please enter root password for device:"
read PASSWD

ncftp -u $USER -p $PASSWD $HOST <<END_SCRIPT
binary
cd /mnt/storage/
mput -R ka-lite
cd /etc/rc.d/init.d/service/
put config/S90kalite
quit
END_SCRIPT
