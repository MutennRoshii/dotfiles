#!/usr/bin/env bash

dir="/home/roshi/.config/rofi"
rofi_command="rofi -theme $dir/powermenu-center.rasi"

uptime=$(uptime -p | sed -e 's/up //g')

# Options
shutdown=""
reboot=""
lock=""
suspend=""
logout="﫻"

# Variable passed to rofi
options="$shutdown\n$reboot\n$lock\n$suspend\n$logout"

chosen="$(echo -e "$options" | $rofi_command -p "祥  $uptime " -dmenu -selected-row 2)"
case $chosen in
    $shutdown)
		systemctl poweroff
        ;;
    $reboot)
		systemctl reboot
        ;;
    $lock)
		betterlockscreen -l
        ;;
    $suspend)
		systemctl suspend
        ;;
    $logout)
		loginctl terminate-session ${XDG_SESSION_ID-}
        ;;
esac
