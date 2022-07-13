#!/usr/bin/env bash

dir="/home/roshi/.config/rofi"
rofi_command="rofi -theme $dir/network-applet.rasi"

## Get info
IFACE="$(nmcli | grep -i interface | awk '/interface/ {print $2}')"
#SSID="$(iwgetid -r)"
#LIP="$(nmcli | grep -i server | awk '/server/ {print $2}')"
#PIP="$(dig +short myip.opendns.com @resolver1.opendns.com )"
STATUS="$(nmcli radio wifi)"

active=""
urgent=""

if (ping -c 1 archlinux.org || ping -c 1 google.com || ping -c 1 bitbucket.org || ping -c 1 github.com || ping -c 1 sourceforge.net) &>/dev/null; then
	if [[ $STATUS == *"enable"* ]]; then
        if [[ $IFACE == e* ]]; then
            connected=" "
        else
            connected=" "
        fi
	active="-a 0"
	SSID=" $(nmcli connection show --active | grep 'wifi' | awk '{ print $1 }' FS='  ')"
	PIP="$(wget --timeout=30 http://ipinfo.io/ip -qO -)"
	fi
else
    urgent="-u 0"
    SSID="Disconnected"
    PIP="Not Available"
    connected=" "
fi

## Icons
list=" "
launch="漣 "

options="$connected\n$list\n$launch"

## Main
chosen="$(echo -e "$options" | $rofi_command -p "$SSID" -dmenu $active $urgent -selected-row 1)"
case $chosen in
    $connected)
		if [[ $STATUS == *"enable"* ]]; then
			nmcli radio wifi off
		else
			nmcli radio wifi on
		fi 
        ;;
    $list)
        ${dir}/wifi-menu.sh
        ;;
    $launch)
        nm-connection-editor
        ;;
esac
