# -*- coding:utf-8 -*-
# my-packages
from visualizer.algorithms.sort import BubbleSort

if __name__ == '__main__':
    data = [2, 4, 3, 1]
    sorter = BubbleSort()
    sorter.set_data(data)
    sorter.run()
    print(sorter.get_data())
