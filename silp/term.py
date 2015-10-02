import sys

import lnkr

def fake_color(str):
    return str

class WinTerminal:
    def __init__(self):
        self.normal = fake_color
        self.red = fake_color
        self.green = fake_color
        self.blue = fake_color
        self.yellow = fake_color

windows_mode = sys.platform.startswith('win')

def get_terminal():
    if windows_mode:
        term = WinTerminal()
    else:
        from blessings import Terminal
        term = Terminal()
    return term

term = get_terminal()
verbose_mode = False

def set_verbose_mode(mode):
    global verbose_mode
    verbose_mode = mode

def info(msg):
    if windows_mode:
        print msg
    else:
        print term.normal + msg

def verbose(msg):
    if verbose_mode:
        info(msg)

def error(msg):
    if windows_mode:
        print msg
    else:
        print term.red + msg

def format_error(err):
    return term.red(err)

def format_path(path):
    return term.blue(path)

def format_param(param):
    return term.yellow(param)

