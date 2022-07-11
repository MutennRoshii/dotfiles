#!/bin/bash

cp -r ~/.config/dunst ./config/
cp -r ~/.config/kitty ./config/
cp -r ~/.config/nvim ./config/
cp -r ~/.config/picom ./config/
cp -r ~/.config/qtile ./config/
cp -r ~/.config/rofi ./config/

cp ~/.local/bin/scripts/* ./scripts/

paru -Qetq > ./packages
