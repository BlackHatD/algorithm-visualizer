# -*- coding:utf-8 -*-
# my-packages
from visualizer.algorithm import AbstractAlgorithm

__all__ = ['QuickSort']

class QuickSort(AbstractAlgorithm):
    """QuickSort"""
    def run(self):
        dataset = self.dataset

        def __recursive(start_index, end_index):
            ## set pivot
            pivot = dataset[(start_index + end_index) // 2]

            left_index  = start_index
            right_index = end_index

            self.draw((left_index, 'Blue'), (right_index, 'Blue'))
            self.sleep()

            while True:
                ## find a value bigger than the pivot
                ## from the left side
                while dataset[left_index] < pivot:
                    left_index += 1

                ## find a value smaller than the pivot
                ## from the right side
                while pivot < dataset[right_index]:
                    right_index -= 1

                if right_index <= left_index:
                    break

                self.swap(left_index, right_index)

                left_index  += 1
                right_index -= 1

            if start_index < left_index - 1:
                __recursive(start_index=start_index, end_index=(left_index - 1))

            if right_index + 1 < end_index:
                __recursive(start_index=(right_index + 1), end_index=end_index)

        __recursive(0, len(dataset)-1)

        self.draw_all('Yellow')

