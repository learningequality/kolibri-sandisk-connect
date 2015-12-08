#!/bin/sh
HOST='192.168.11.1'
USER='root'

echo "Please enter root password for device:"
read PASSWD

ncftp -u $USER -p $PASSWD $HOST <<END_SCRIPT
cd /mnt/storage/
binary
cd /etc/init.d/service/
put files/service/*
cd /root
mkdir scripts
cd scripts
put files/scripts/*
quit
END_SCRIPT

scripts/_run_config_scripts.sh $PASSWD
