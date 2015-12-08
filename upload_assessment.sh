#!/bin/sh
HOST='192.168.11.1'
USER='root'

echo "Please enter root password for device:"
read PASSWD

ncftp -u $USER -p $PASSWD $HOST <<END_SCRIPT
cd /mnt/storage/ka-lite/content/assessment/khan
binary
put khan_assessment.zip
quit
END_SCRIPT
