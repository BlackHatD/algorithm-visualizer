# -*- coding:utf-8 -*-
# builtins
import random

# my-packages
from visualizer.algorithms.sort import BubbleSort

if __name__ == '__main__':
    data = [(i+1) for i in range(1000)]
    sorter = BubbleSort()
    sorter.set_data(random.sample(data, len(data)))
    sorter.run()

    assert data == sorter.get_data(), sorter.get_data()
