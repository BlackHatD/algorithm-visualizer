# -*- coding:utf-8 -*-
# my-packages
from algorithms.sort import Bubble

if __name__ == '__main__':
    data = [2, 4, 3, 1]
    sorter = Bubble()
    sorter.set_data(data)
    sorter.run()
    print(sorter.get_data())
