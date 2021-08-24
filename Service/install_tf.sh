#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "This script must be run as root (use sudo)" 1>&2
	exit 1
fi

cp tf /usr/bin/
cp tf.service /etc/systemd/system/
systemctl enable tf.service
systemctl start tf

exit 0

