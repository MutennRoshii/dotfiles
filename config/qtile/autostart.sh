#!/bin/sh

# Autostart script for Qtile

cmd_exist() { unalias "$1" >/dev/null 2>&1 ; command -v "$1" >/dev/null 2>&1 ;}
__kill() { kill -9 "$(pidof "$1")" >/dev/null 2>&1 ; }
__start() { sleep 1 && "$@" >/dev/null 2>&1 & }
__running() { pidof "$1" >/dev/null 2>&1 ;}

# Apps to autostart

# Set the wallpaper using either feh or nitrogen
if cmd_exist nitrogen ; then
    __kill nitrogen
    __start nitrogen --restore
fi

# Compositor
if cmd_exist picom ; then
    __kill picom
    __start picom
fi

# Authentication dialog
if [ -f /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 ]; then
    __kill polkit-gnome-authentication-agent-1
    __start /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1
fi

# Notification daemon
if cmd_exist dunst ; then
    __kill dunst
    __start dunst
fi

# Clipboard daemon
if cmd_exist clipmenud ; then
    __kill clipmenud
    __start clipmenud
fi

# Bluetooth applet
if cmd_exist blueman-applet ; then
    __kill blueman-applet
    __start blueman-applet
fi

# Unclutter
if cmd_exist unclutter ; then
    __kill unclutter
    __start unclutter
fi

/home/roshi/.local/bin/scripts/screenlayout.sh
