#!/bin/bash
cd /lib/modules/4.1.15/
modprobe 8188eu
ifconfig wlan0 up
wpa_supplicant -D wext -c /etc/wpa_supplicant.conf -i wlan0 &
udhcpc -i wlan0
