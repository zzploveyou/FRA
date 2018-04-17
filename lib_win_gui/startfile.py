# coding:utf-8
from sys import platform as pf
import os


def start(filename):
    if pf == 'win32':
        os.startfile(filename)
    elif pf == 'linux2':
        order = "xdg-open {}".format(filename)
        os.system(order)
    elif pf == 'darwin':
        os.system("open {}".format(filename))
    else:
        pass
