from sqlite3 import Cursor
from typing import List
from libqtile import qtile
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.layout.floating import Floating
from libqtile.lazy import lazy
from libqtile import hook
from datetime import datetime as dt
import os
import subprocess
import time

mod = 'mod4'
alt = 'mod1'
terminal = 'kitty'
browser = 'firefox'
home = os.path.expanduser('~')
rofi = os.path.expanduser('~/.config/rofi/')
scripts = os.path.expanduser('~/.local/bin/scripts/')


# Get the number of connected screens

def get_monitors():
    xr = subprocess.check_output(
        'xrandr --query | grep " connected"', shell=True).decode().split('\n')
    monitors = len(xr) - 1 if len(xr) > 2 else len(xr)
    return monitors


monitors = get_monitors()


@hook.subscribe.screen_change
def set_screens(event):
    subprocess.run("screenlayout.sh")
    qtile.restart()


# When application launched automatically focus it's group

@hook.subscribe.client_new
def modify_window(client):
    for group in groups:  # follow on auto-move
        match = next((m for m in group.matches if m.compare(client)), None)
        if match:
            # there can be multiple instances of a group
            targetgroup = client.qtile.groups_map[group.name]
            targetgroup.cmd_toscreen(toggle=False)
            break


# Hook to fallback to the first group with windows when last window of group is killed

@hook.subscribe.client_killed
def fallback(window):
    if window.group.windows != [window]:
        return
    idx = qtile.groups.index(window.group)
    for group in qtile.groups[idx - 1::-1]:
        if group.windows:
            qtile.current_screen.toggle_group(group)
            return
    qtile.current_screen.toggle_group(qtile.groups[0])


@hook.subscribe.client_new
def slight_delay(window):
    time.sleep(0.04)


@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])


# Add th, nd or st to the date - use custom_date in text box

def suffix(d):
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))


def custom_date():
    return custom_strftime('%A {S} %B %Y - %H:%M', dt.now())


COLORS = {
    "Rosewater":    "#f5e0dc",
    "Flamingo":     "#f2cdcd",
    "Pink":         "#f5c2e7",
    "Mauve":        "#cba6f7",
    "Red":          "#f38ba8",
    "Maroon":       "#eba0ac",
    "Peach":        "#fab387",
    "Yellow":       "#f9e2af",
    "Green":        "#a6e3a1",
    "Teal":         "#94e2d5",
    "Sky":          "#89dceb",
    "Sapphire":     "#74c7ec",
    "Blue":         "#89b4fa",
    "Lavender":     "#b4befe",
    "Text":         "#cdd6f4",
    "Subtext1":     "#bac2de",
    "Subtext0":     "#a6adc8",
    "Overlay2":     "#9399b2",
    "Overlay1":     "#7f849c",
    "Overlay0":     "#6c7086",
    "Surface2":     "#585b70",
    "Surface1":     "#45475a",
    "Surface0":     "#313244",
    "Base":         "#1e1e2e",
    "Mantle":       "#181825",
    "Darkblue":     "#091a32",
    "Crust":        "#11111b"
}

COLOR_1 = "#11111b"
COLOR_2 = "#f38ba8"
COLOR_3 = "#fab387"
COLOR_4 = "#091a32"
COLOR_5 = "#1e1e2e"
COLOR_6 = "#45475a"

keys = [

    # ------------  Window Management ------------
    Key([mod],              "h",        lazy.layout.left(),
        desc="Move focus left"),
    Key([mod],              "l",        lazy.layout.right(),
        desc="Move focus right"),
    Key([mod],              "j",        lazy.layout.down(),
        desc="Move focus down"),
    Key([mod],              "k",        lazy.layout.up(),
        desc="Move focus up"),
    Key([mod],              "space",    lazy.layout.next(),
        desc="Move focus next"),

    Key([mod, "shift"],     "h",        lazy.layout.shuffle_left(),
        desc="Move window left"),
    Key([mod, "shift"],     "l",        lazy.layout.shuffle_right(),
        desc="Move window right"),
    Key([mod, "shift"],     "j",        lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"],     "k",        lazy.layout.shuffle_up(),
        desc="Move window up"),

    Key([mod, "control"],   "h",        lazy.layout.grow_left(),
        desc="Grow window left"),
    Key([mod, "control"],   "l",        lazy.layout.grow_right(),
        desc="Grow window right"),
    Key([mod, "control"],   "j",        lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"],   "k",        lazy.layout.grow_up(),
        desc="Grow window up"),

    Key([mod, "shift"],     "f",        lazy.window.toggle_floating(),
        desc="Toggle floating"),
    Key([mod],              "Tab",      lazy.next_layout(),
        desc="Toggle layouts"),
    Key([mod],              "n",        lazy.layout.normalize(),
        desc="Reset window sizes"),
    Key([mod],              "m",        lazy.layout.maximize(),
        desc='Toggle max size'),
    Key([mod],              "f",        lazy.window.toggle_fullscreen(),
        desc='Toggle fullscreen'),

    Key([mod],              "w",        lazy.window.kill(),
        desc="Kill focused window"),
    Key([mod, "control"],   "r",        lazy.restart(),
        desc="Restart qtile"),
    Key([mod, "control"],   "q",        lazy.shutdown(),
        desc="Shutdown qtile"),

    # ------------  Launch Commands   ------------
    Key([mod, "control"],   "p",        lazy.spawn(rofi + "powermenu-center.sh"),
        desc="Launch Power menu"),
    Key(["control"],        "space",    lazy.spawn(rofi + "launcher.sh"),
        desc="Launch Rofi menu"),
    Key([mod], 				"c", 		lazy.spawn("clipmenu"),
        desc="Launch clipboard"),
    Key([mod],              "Return",   lazy.spawn(terminal),
        desc="Launch terminal"),
    Key([mod],              'b',        lazy.spawn(browser),
        desc="Launch browser"),

    # ------------  Hardware Configs  ------------
    Key([], "XF86AudioMute",            lazy.spawn(scripts + "changevolume mute"),
        desc='Mute audio'),
    Key([], "XF86AudioLowerVolume",     lazy.spawn(scripts + "changevolume down"),
        desc='Volume down'),
    Key([], "XF86AudioRaiseVolume",     lazy.spawn(scripts + "changevolume up"),
        desc='Volume up'),

    Key([], "XF86MonBrightnessDown",    lazy.spawn(scripts + "changebrightness down"),
        desc='Brightness down'),
    Key([], "XF86MonBrightnessUp",      lazy.spawn(scripts + "changebrightness up"),
        desc='Brightness up'),

    Key([],                 "Print",    lazy.spawn(scripts + "screenshot"),
        desc='Take screen'),
    Key([mod],              "Print",    lazy.spawn(scripts + "screenshot window"),
        desc='Take screen of Window'),
    Key([mod, "shift"],     "s",        lazy.spawn(scripts + "screenshot select"),
        desc='Take screen of Region'),
]

# Groups with matches
# Japanese Kanji: 一二三四五六七八九            

workspaces = [
    {"name": " ", "key": "ampersand",  "matches": [
        Match(wm_class='firefox')], 	"layout": "columns"},
    {"name": " ", "key": "eacute",     "matches": [
        Match(wm_class='kitty')],   	"layout": "columns"},
    {"name": " ", "key": "quotedbl",   "matches": [
        Match(wm_class='code')],    	"layout": "columns"},
    {"name": " ", "key": "apostrophe", "matches": [
        Match(wm_class='kodi')],		"layout": "columns"},
    {"name": " ", "key": "parenleft",  "matches": [
        Match(wm_class='gimp')],    	"layout": "columns"},
    {"name": " ", "key": "section",    "matches": [
        Match(wm_class='spotify')],     "layout": "columns"},
    {"name": " ", "key": "egrave",     "matches": [
        Match(wm_class='zathura')],     "layout": "columns"},
    {"name": " ", "key": "exclam",     "matches": [
        Match(wm_class='retroarch')],   "layout": "columns"},
    {"name": " ", "key": "ccedilla",   "matches": [
        Match(wm_class='discord')],     "layout": "columns"},
]

groups = []
for workspace in workspaces:
    matches = workspace["matches"] if "matches" in workspace else None
    layouts = workspace["layout"] if "layout" in workspace else None
    groups.append(Group(workspace["name"], matches=matches, layout=layouts))
    keys.append(Key([mod], workspace["key"],
                    lazy.group[workspace["name"]].toscreen()))
    keys.append(Key([mod, "shift"], workspace["key"],
                    lazy.window.togroup(workspace["name"])))

# Move window to screen with Mod, Alt and number


for i in range(monitors):
    keys.extend([Key([mod, "mod1"], str(i), lazy.window.toscreen(i))])

# DEFAULT THEME SETTINGS FOR LAYOUTS #
layout_theme = {
    "border_width":     2,
    "margin":           8,
    "border_focus":     COLORS["Mauve"],
    "border_normal":    COLORS["Crust"]
}

layouts = [
    layout.Columns(**layout_theme),
    layout.MonadTall(**layout_theme, single_border_width=0),
    layout.Max(),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
]

widget_defaults = dict(
    font='JetBrainsMono Medium Nerd Font',
    fontsize=17,
    padding=3,
)

pl_defaults = dict(
    font='JetBrainsMono Nerd Font',
    fontsize=28,
    padding=0
)

group_defaults = dict(
    font='JetBrainsMono Nerd Font',
    fontsize=28,
    padding=0
)

screens = []

# ZeroNet.svg
menu_svg = '/usr/share/icons/Papirus-Dark/16x16/apps/'
menu_svg += 'void-wizard.svg'

widget_mirror = [
    widget.CheckUpdates(
        **widget_defaults,
        background=COLOR_3,
        foreground=COLOR_5,
        colour_have_updates=COLOR_5,
        update_interval=1800,
        custom_command='paru -Qu',
        display_format=' {updates}',
        execute=terminal + ' -e paru',
        distro='Arch',
    ),
    widget.GenPollText(
        **widget_defaults,
        background=COLOR_3,
        foreground=COLOR_5,
        update_interval=None,
        func=lambda: subprocess.check_output(
            scripts + "changebrightness").decode(),
        mouse_callbacks={
            'Button5': lambda: qtile.cmd_spawn(scripts + "changebrightness down", shell=True),
            'Button4': lambda: qtile.cmd_spawn(scripts + "changebrightness up", shell=True)}
    ),
    widget.GenPollText(
        **widget_defaults,
        background=COLOR_3,
        foreground=COLOR_5,
        update_interval=None,
        func=lambda: subprocess.check_output(
            scripts + "changevolume").decode(),
        mouse_callbacks={
            'Button5': lambda: qtile.cmd_spawn(scripts + "changevolume down", shell=True),
            'Button2': lambda: qtile.cmd_spawn(scripts + "changevolume mute", shell=True),
            'Button4': lambda: qtile.cmd_spawn(scripts + "changevolume up", shell=True)}
    ),
    widget.GenPollText(
        **widget_defaults,
        background=COLOR_3,
        foreground=COLOR_5,
        update_interval=1,
        func=lambda: subprocess.check_output(scripts + "battery.py").decode(),
        mouse_callbacks={
            'Button1': lambda: qtile.cmd_spawn(scripts + "battery.py --c left-click", shell=True)}
    ),
    widget.TextBox(
        **pl_defaults,
        fmt='',
        background=COLOR_3,
        foreground=COLOR_2,
    ),
    widget.GenPollText(
        **widget_defaults,
        background=COLOR_2,
        foreground=COLOR_5,
        update_interval=1,
        func=lambda: subprocess.check_output(scripts + "network.sh").decode(),
        mouse_callbacks={
            'Button1': lambda: qtile.cmd_spawn(rofi + "network-applet.sh", shell=True),
            'Button3': lambda: qtile.cmd_spawn(rofi + 'wifi-menu.sh', shell=True)}
    ),
    widget.TextBox(
        **widget_defaults,
        background=COLOR_2,
        foreground=COLOR_5,
        text=' ',
        mouse_callbacks={
            'Button1': lazy.spawn("/home/roshi/.config/rofi/powermenu-applet.sh")}
    ),
    widget.Spacer(
        length=5,
        background=COLOR_2
    ),
]

widgets_1 = [
    widget.Spacer(
        length=10,
        background=COLOR_2
    ),
    widget.Image(
        background=COLOR_2,
        filename=menu_svg,
        rotate=270,
        mouse_callbacks={
            'Button1': lazy.spawn(rofi + "launcher.sh")}
    ),
    widget.TextBox(
        **pl_defaults,
        fmt='',
        background=COLOR_3,
        foreground=COLOR_2
    ),
    widget.GroupBox(
        **group_defaults,
        disable_drag=True,
        highlight_method='line',
        borderwidth=3,
        active=COLOR_5,
        inactive=COLOR_6,
        background=COLOR_3,
        this_current_screen_border=COLOR_5,
        this_screen_border=COLOR_5,
        highlight_color=[COLOR_3, COLOR_3]
    ),
    widget.TextBox(
        **pl_defaults,
        fmt='',
        background=COLOR_4,
        foreground=COLOR_3
    ),
    widget.CurrentLayoutIcon(
        scale=0.80,
        background=COLOR_4,
    ),
    widget.CurrentLayout(
        **widget_defaults,
        background=COLOR_4,
    ),
    widget.TextBox(
        **pl_defaults,
        fmt='',
        background=COLOR_1,
        foreground=COLOR_4
    ),
    widget.Spacer(),
    widget.GenPollText(
        font='JetBrainsMono Medium Nerd Font',
        fontsize='18',
        padding=3,
        func=custom_date,
        update_interval=1,
    ),
    widget.Spacer(),
    widget.WidgetBox(
        **pl_defaults,
        widgets=[
            widget.Spacer(length=5, background=COLOR_4),
            widget.Systray(background=COLOR_4)
        ],
        background=COLOR_1,
        foreground=COLOR_4,
        text_closed="",
        text_open=""),
    widget.Spacer(
        length=5,
        background=COLOR_4,
    ),
    widget.TextBox(
        **pl_defaults,
        fmt='',
        background=COLOR_4,
        foreground=COLOR_3,
    ),
] + widget_mirror

widgets_2 = [
    widget.Spacer(
        length=10,
        background=COLOR_2
    ),
    widget.Image(
        background=COLOR_2,
        filename=menu_svg,
        rotate=270,
        mouse_callbacks={
            'Button1': lazy.spawn(rofi + "launcher.sh")}
    ),
    widget.TextBox(
        **pl_defaults,
        fmt='',
        background=COLOR_3,
        foreground=COLOR_2
    ),
    widget.GroupBox(
        **group_defaults,
        disable_drag=True,
        highlight_method='line',
        borderwidth=3,
        active=COLOR_5,
        inactive=COLOR_6,
        background=COLOR_3,
        this_current_screen_border=COLOR_5,
        this_screen_border=COLOR_5,
        highlight_color=[COLOR_3, COLOR_3]
    ),
    widget.TextBox(
        **pl_defaults,
        fmt='',
        background=COLOR_4,
        foreground=COLOR_3
    ),
    widget.CurrentLayoutIcon(
        scale=0.80,
        background=COLOR_4,
    ),
    widget.CurrentLayout(
        **widget_defaults,
        background=COLOR_4,
    ),
    widget.TextBox(
        **pl_defaults,
        fmt='',
        background=COLOR_1,
        foreground=COLOR_4
    ),
    widget.Spacer(),
    widget.GenPollText(
        font='JetBrainsMono Medium Nerd Font',
        fontsize='18',
        padding=3,
        func=custom_date,
        update_interval=1,
    ),
    widget.Spacer(),
    widget.TextBox(
        **pl_defaults,
        fmt='',
        background=COLOR_1,
        foreground=COLOR_3,
    ),
] + widget_mirror


for monitor in range(monitors):
    if monitor == 0:
        screens.append(
            Screen(top=bar.Bar(widgets_1, 30, background=COLOR_1, margin=0)))  # [4, 8, 0, 8]
    else:
        screens.append(
            Screen(top=bar.Bar(widgets_2, 30, background=COLOR_1, margin=0)))


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # *layout.Floating.default_float_rules,
    Match(title='Quit and close tabs?'),
    Match(wm_type='utility'),
    Match(wm_type='notification'),
    Match(wm_type='toolbar'),
    Match(wm_type='splash'),
    Match(wm_type='dialog'),
    Match(wm_class='Conky'),
    Match(wm_class='Firefox'),
    Match(wm_class='feh'),
    Match(wm_class='file_progress'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='blueman-manager'),
    Match(wm_class='nm-connection-editor'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
],
    border_width=0
)
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
