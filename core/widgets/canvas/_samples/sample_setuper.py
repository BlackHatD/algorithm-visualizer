# -*- coding:utf-8 -*-
# builtins
import tkinter as tk

# my-packages
from core.data import DataObj
from core.widgets.canvas import DrawUtilKeys, DrawUtil


__all__ = ['root', 'DataObj', 'DrawUtilKeys', 'DrawUtil', 'setuper']

root = tk.Tk()

def setuper(dataset):
    ## setup widgets
    w_canvas = tk.Canvas(root)
    w_canvas.pack(fill=tk.BOTH, expand=True)

    ## create an instance
    drawer = DrawUtil()
    drawer.attach(w_canvas)

    ## initialize dataset
    drawer.init_dataset(dataset)

    ## setup dataset
    drawer.setup_dataset(dataset)

    return drawer

