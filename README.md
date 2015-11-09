ka-lite-sandisk-connect
=======================

## Prerequisites

sudo apt-get install expect ncftp git

## Getting started

- Clone this repository with --recursive, so you get the ka-lite submodule
- Run ./build_python.sh to download all the necessary files (including a large toolchain) to cross-compile Python for Freescale ARM.
- Run ./upload_python.sh, ./upload_kalite.sh, and ./upload_config_and_scripts.sh to copy the appropriate files to the device.
- Telnet into the device and run /mnt/storage/ka-lite/setup_unix.sh to configure the KA Lite database for the first time.
- Copy the KA Lite videos/screenshots into the /mnt/storage/ka-lite/content directory, using FTP or over USB.
- Reboot the device and wait a few minutes for KA Lite to load, then access it at: http://192.168.11.1:8008/