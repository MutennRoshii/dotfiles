#!/bin/bash

# Config Backups
cp -r /home/roshi/.config/dunst ./config/
cp -r /home/roshi/.config/kitty ./config/
cp -r /home/roshi/.config/nvim ./config/
cp -r /home/roshi/.config/obsidian ./config/
cp -r /home/roshi/.config/picom ./config/
cp -r /home/roshi/.config/qtile ./config/
cp -r /home/roshi/.config/rofi ./config/

# Icon Backups
# cp -r /home/roshi/.local/share/icons/* ./icons/
# cp -r /usr/share/icons/Simp1e-Catppuccin ./icons/
# cp -r /usr/share/icons/Papirus ./icons/
# cp -r /usr/share/icons/Papirus-Dark ./icons/

# Theme Backups
# cp -r /usr/share/themes/Catppuccin-pink ./themes/

# Script Backups
cp /home/roshi/.local/bin/scripts/* ./scripts/

# Package List Backup
paru -Qetq > ./packages
