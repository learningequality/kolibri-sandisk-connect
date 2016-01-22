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
send "cd /mnt/storage/\n"

expect "Media_Drive"
send "tar -xvzf setuptools-18.4.tar.gz\n"

expect "Media_Drive"
send "rm -r python\n"

expect "Media_Drive"
send "mkdir python\n"

expect "Media_Drive"
send "cd python\n"

expect "Media_Drive"
send "unzip ../python.zip\n"

expect "Media_Drive"
send "rm /usr/bin/python 2> /dev/null; ln -s /mnt/storage/python/bin/python /usr/bin/python\n"

expect "Media_Drive"
send "rm /bin/python 2> /dev/null; echo 'PYTHONHOME=/usr/ /usr/bin/python $@' > /bin/python; chmod +x /bin/python\n"

expect "Media_Drive"
send "mkdir -p /usr/include\n"

expect "Media_Drive"
send "rm /usr/include/python2.7 2> /dev/null; ln -s /mnt/storage/python/usr/include/python2.7 /usr/include/python2.7\n"

expect "Media_Drive"
send "mkdir -p /usr/lib\n"

expect "Media_Drive"
send "rm /usr/lib/python2.7 2> /dev/null; ln -s /mnt/storage/python/usr/lib/python2.7 /usr/lib/python2.7\n"

expect "Media_Drive"
send "rm /usr/lib/python27.zip 2> /dev/null; ln -s /mnt/storage/python/usr/lib/python27.zip /usr/lib/python27.zip\n"

expect "Media_Drive"
send "cd /mnt/storage/setuptools-18.4\n"

expect "Media_Drive"
send "python setup.py install\n"

expect "Media_Drive"
send "cd /var/ftp/storage/; dd if=/dev/zero of=/var/ftp/storage/temp.bin bs=1 count=0 seek=1G; 
      mkfs.ext4 /var/ftp/storage/temp.bin\n" 

expect "Media_Drive"
send "y\n"

expect "Media_Drive"
send "mount -o loop,rw,nodev,noexec /var/ftp/storage/temp.bin /tmp\n"

expect "Media_Drive"
send "exit\n";
interact

