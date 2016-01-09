#! /bin/bash

apt-get update
apt-get install  libasound2-dev memcahed python-pip python-alsaaudio
pip install -r requirements.txt
cp initd_alexa.sh /etc/init.d/alexa
cd /etc/rc5.d
ln -s ../init.d/alexa S99alexa
touch /var/log/alexa.log

echo "You can now reboot"
