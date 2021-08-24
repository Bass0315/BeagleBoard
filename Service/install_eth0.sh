#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "This script must be run as root (use sudo)" 1>&2
	exit 1
fi

cp eth0 /usr/bin/
cp eth0.service /etc/systemd/system/
systemctl enable eth0.service
systemctl start eth0

exit 0

