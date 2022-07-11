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
browser = 'firefox'
terminal = 'kitty'
home = os.path.expanduser('~')
scripts = os.path.expanduser('~/.local/bin/scripts/')
rofi = os.path.expanduser('~/.config/rofi/')

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


MYCOLORS = [
    '#141c21',
    '#fb4934',
    '#A9C03F',
    '#FDD835',
    '#4DD0E1',
    '#F75176',
    '#00B19F',
    '#eee8d5'
]

BLACK = MYCOLORS[0]
RED = MYCOLORS[1]
GREEN = MYCOLORS[2]
YELLOW = MYCOLORS[3]
BLUE = MYCOLORS[4]
MAGENTA = MYCOLORS[5]
CYAN = MYCOLORS[6]
WHITE = MYCOLORS[7]

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
# Japanese Kanji: 一二三四五六七八九

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
    "border_focus":     MAGENTA,
    "border_normal":    BLACK
}

layouts = [
    layout.Columns(**layout_theme),
    layout.MonadTall(**layout_theme, single_border_width=0),
    layout.Max(),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),

    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.Stack(num_stacks=2, **layout_theme),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='JetBrainsMono Nerd Font',
    fontsize='18',
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = []

# ZeroNet.svg
menu_svg = '~/.local/share/icons/Papirus-Dark/16x16/apps/'
menu_svg += 'void-wizard.svg'

widget_mirror = [
    widget.CheckUpdates(
        **widget_defaults,
        update_interval=1800,
        distro='Arch',
        custom_command='paru -Qu',
        display_format=' {updates}',
        colour_have_updates=GREEN,
        execute='kitty -e paru',
    ),
    widget.Spacer(length=5),
    widget.GenPollText(
        **widget_defaults,
        update_interval=None,
        func=lambda: subprocess.check_output(
            scripts + "changebrightness").decode(),
        mouse_callbacks={
            'Button5': lambda: qtile.cmd_spawn(scripts + "changebrightness down", shell=True),
            'Button4': lambda: qtile.cmd_spawn(scripts + "changebrightness up", shell=True)}
    ),
    widget.Spacer(length=5),
    widget.GenPollText(
        **widget_defaults,
        update_interval=None,
        func=lambda: subprocess.check_output(
            scripts + "changevolume").decode(),
        mouse_callbacks={
            'Button5': lambda: qtile.cmd_spawn(scripts + "changevolume down", shell=True),
            'Button2': lambda: qtile.cmd_spawn(scripts + "changevolume mute", shell=True),
            'Button4': lambda: qtile.cmd_spawn(scripts + "changevolume up", shell=True)}
    ),
    widget.Spacer(length=5),
    widget.GenPollText(
        **widget_defaults,
        update_interval=1,
        func=lambda: subprocess.check_output(scripts + "battery.py").decode(),
        mouse_callbacks={
            'Button1': lambda: qtile.cmd_spawn(scripts + "battery.py --c left-click", shell=True)}
    ),
    widget.Spacer(length=5),
    widget.GenPollText(
        **widget_defaults,
        update_interval=1,
        func=lambda: subprocess.check_output(scripts + "network.sh").decode(),
        mouse_callbacks={
            'Button1': lambda: qtile.cmd_spawn(scripts + "network.sh ShowInfo", shell=True),
            'Button3': lambda: qtile.cmd_spawn(rofi + 'wifi-menu.sh', shell=True)}
    ),
    widget.TextBox(
        **widget_defaults,
        text='  ',
        mouse_callbacks={
            'Button1': lazy.spawn("/home/roshi/.config/rofi/powermenu-applet.sh")}
    )
]

widgets_1 = [
    widget.Spacer(length=10),
    widget.Image(
        filename=menu_svg,
        rotate=270,
        mouse_callbacks={
            'Button1': lazy.spawn(rofi + "launcher.sh")}
    ),
    widget.Spacer(length=5),
    widget.GroupBox(
        borderwidth=2,
        disable_drag=True,
        active=WHITE,
        inactive='#969696',
        this_current_screen_border=MAGENTA,
        this_screen_border=MAGENTA,
        font='JetBrainsMono Nerd Font',
        fontsize=26,
        highlight_method='line',
        highlight_color=['141c2100', '141c2100']
    ),
    widget.Spacer(length=5),
    widget.CurrentLayoutIcon(scale=0.7),
    widget.CurrentLayout(
        font='JetBrainsMono Nerd Font',
        fontsize='16',
        padding=3,),
    widget.Prompt(**widget_defaults),
    widget.Spacer(),
    widget.GenPollText(
        func=custom_date,
        update_interval=1,
        font='JetBrainsMono Nerd Font',
        fontsize='16',
        padding=3,
    ),
    widget.Spacer(),
    widget.WidgetBox(
        widgets=[widget.Systray()],
        font='JetBrainsMono Nerd Font',
        fontsize=32,
        foreground='#9e4174',
        close_button_location='left',
        text_closed="",
        text_open=""),
] + widget_mirror

widgets_2 = [
    widget.Spacer(length=10),
    widget.Image(
        filename=menu_svg,
        rotate=270,
        mouse_callbacks={
            'Button1': lazy.spawn(rofi + "launcher.sh")}
    ),
    widget.Spacer(length=5),
    widget.GroupBox(
        borderwidth=2,
        disable_drag=True,
        active=WHITE,
        inactive='#969696',
        this_current_screen_border=MAGENTA,
        this_screen_border=MAGENTA,
        font='JetBrainsMono Nerd Font',
        fontsize=26,
        highlight_method='line',
        highlight_color=['141c2100', '141c2100']
    ),
    widget.Spacer(length=5),
    widget.CurrentLayoutIcon(scale=0.7),
    widget.CurrentLayout(
        font='JetBrainsMono Nerd Font',
        fontsize='16',
        padding=3,
    ),
    widget.Prompt(**widget_defaults),
    widget.Spacer(),
    widget.GenPollText(
        func=custom_date,
        update_interval=1,
        font='JetBrainsMono Nerd Font',
        fontsize='16',
        padding=3,
    ),
    widget.Spacer(),
] + widget_mirror


for monitor in range(monitors):
    if monitor == 0:
        screens.append(
            Screen(top=bar.Bar(widgets_1, 30, background="#141c21", margin= [4, 8, 0, 8])))
    else:
        screens.append(
            Screen(top=bar.Bar(widgets_2, 30, background="#141c21", margin= [4, 8, 0, 8])))


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
