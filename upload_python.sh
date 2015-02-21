#!/bin/sh
HOST='192.168.11.1'
USER='root'

cd pybuild

echo "Please enter root password for device:"
read PASSWD

ncftp -u $USER -p $PASSWD $HOST <<END_SCRIPT
cd /mnt/storage/
binary
put python.zip
quit
END_SCRIPT

../scripts/_install_python.sh $PASSWD

cd ..