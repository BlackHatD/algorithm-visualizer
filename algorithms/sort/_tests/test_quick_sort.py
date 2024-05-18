# -*- coding:utf-8 -*-
# builtins
import random

# my-packages
from algorithms.sort import QuickSort

if __name__ == '__main__':
    data = [(i+1) for i in range(1000)]
    sorter = QuickSort()
    sorter.set_data(random.sample(data, len(data)))
    sorter.run()

    assert data == sorter.get_data(), sorter.get_data()
