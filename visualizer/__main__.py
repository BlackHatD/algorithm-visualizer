# -*- coding:utf-8 -*-
# my-packages
from visualizer.core import Visualizer
from visualizer.algorithms.sort import Bubble, QuickSort

if __name__ == '__main__':

    v = Visualizer()
    v.register(Bubble, QuickSort)
    v.init()

    v.mainloop()