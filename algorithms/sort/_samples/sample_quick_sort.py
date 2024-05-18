# -*- coding:utf-8 -*-
# my-packages
from algorithms.sort import QuickSort

if __name__ == '__main__':
    data = [2, 4, 3, 1]
    sorter = QuickSort()
    sorter.set_data(data)
    sorter.run()
    print(sorter.get_data())
