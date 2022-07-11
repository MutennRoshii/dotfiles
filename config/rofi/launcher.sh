#!/usr/bin/env bash

theme="launcher"
dir="/home/roshi/.config/rofi"

# accent colors
COLORS=('#EC7875' '#61C766' '#FDD835' '#42A5F5' '#BA68C8' '#4DD0E1' '#00B19F' \
		'#FBC02D' '#E57C46' '#AC8476' '#6D8895' '#EC407A' '#B9C244' '#6C77BB')
ACCENT="${COLORS[$(( $RANDOM % 14 ))]}ff"

rofi -show drun -modi drun -theme $dir/"$theme"
