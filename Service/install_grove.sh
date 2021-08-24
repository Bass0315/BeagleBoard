#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "This script must be run as root (use sudo)" 1>&2
	exit 1
fi

cp grove /usr/bin/
cp grove.service /etc/systemd/system/
systemctl enable grove.service
systemctl start grove

exit 0

