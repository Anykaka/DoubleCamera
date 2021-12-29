#!/bin/bash
insmod 8188eu.ko
ifconfig wlan0 up
wpa_supplicant -D wext -c /etc/wpa_supplicant.conf -i wlan0 &
udhcpc -i wlan0
