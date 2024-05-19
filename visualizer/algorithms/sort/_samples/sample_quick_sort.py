# -*- coding:utf-8 -*-
# my-packages
from visualizer.algorithms.sort import QuickSort

if __name__ == '__main__':
    data = [5, 3, 1, 2, 4]
    sorter = QuickSort()
    sorter.set_data(data)
    sorter.run()
    print(sorter.get_data())
