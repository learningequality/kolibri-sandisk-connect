#!/bin/sh
USER='root'

cd ../pybuild

HOST="$1"
PASSWD="$2"

ncftp -u $USER -p $PASSWD $HOST <<END_SCRIPT
cd /mnt/storage/
binary
put python.zip
put setuptools-18.4.tar.gz
quit
END_SCRIPT

../scripts/_install_python.sh $PASSWD

cd ../ansible/
