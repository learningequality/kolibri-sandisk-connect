#!/bin/sh
HOST='192.168.11.1'
USER='root'

echo "Please enter root password for device:"
read PASSWD

cd ka-lite/dist

ncftp -u $USER -p $PASSWD $HOST <<END_SCRIPT
cd /mnt/storage/
binary
put ka-lite-static-0.16.0.tar.gz
put khan_assessment.zip
quit
END_SCRIPT

../../scripts/_install_kalite.sh $PASSWD
