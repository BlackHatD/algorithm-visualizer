# -*- coding:utf-8 -*-
# builtins
import tkinter as tk
from logging import basicConfig, DEBUG

# site-packages

# my-packages
from visualizer.data import DataObj
from visualizer.widgets.canvas.draw_util import DrawUtil


if __name__ == '__main__':
    basicConfig(level=DEBUG)

    ## setup widgets
    root = tk.Tk()
    w_canvas = tk.Canvas(root)
    w_canvas.pack(fill=tk.BOTH, expand=True)

    ## create a sample dataset
    dataset = DataObj.convert_data_to_dataset([(i+1) for i in range(10)])

    ## create an instance
    drawer = DrawUtil()
    drawer.attach(w_canvas)

    ## initialize dataset
    drawer.init_dataset(dataset)

    ## setup dataset
    drawer.setup_dataset(dataset)


    ## swap data obj
    print(dataset)
    drawer.swap(dataset[0], dataset[9])
    print(dataset)
    drawer.swap(dataset[1], dataset[8])
    print(dataset)
    drawer.swap(dataset[1], dataset[9])
    print(dataset)

    ## draw rectangles
    for data_obj in dataset:
        drawer.draw_rectangle(data_obj, DrawUtil.KEY_DEFAULT_COLOR)
        drawer.draw_value(data_obj, DrawUtil.KEY_DEFAULT_COLOR)

    ## erase objects
    drawer.erase_rectangle(data_obj=dataset[2])


    root.mainloop()
