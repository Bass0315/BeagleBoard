#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "This script must be run as root (use sudo)" 1>&2
	exit 1
fi

cp usb /usr/bin/
cp usb.service /etc/systemd/system/
systemctl enable usb.service
systemctl start usb

exit 0

