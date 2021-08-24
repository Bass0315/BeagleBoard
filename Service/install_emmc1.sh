#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "This script must be run as root (use sudo)" 1>&2
	exit 1
fi

cp emmc1 /usr/bin/
cp emmc1.service /etc/systemd/system/
systemctl enable emmc1.service
systemctl start emmc1

exit 0

