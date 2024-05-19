# -*- coding:utf-8 -*-
# my-packages
from core.algorithm import AbstractAlgorithm

__all__ = ['QuickSort']

class QuickSort(AbstractAlgorithm):
    """QuickSort"""

    def get_current_pivot_index(self, pivot):
        for i in range(len(self.dataset)):
            if self.dataset[i] == pivot:
                return i

    def draw_current_pivot(self, pivot):
        self.draw((self.get_current_pivot_index(pivot), 'Yellow'))

    def draw_area(self, start_index, end_index, pivot):
        area_color  = 'Black'
        self.draw((start_index, area_color), (end_index, area_color))
        self.draw_current_pivot(pivot)


    def run(self):
        dataset = self.dataset

        def get_pivot_index(start_index, end_index):
            return (start_index + end_index) // 2

        def __recursive(start_index, end_index):
            ## set pivot
            ## be careful each data is a DataObj instance's address
            ## so use '.value'
            pivot = dataset[get_pivot_index(start_index, end_index)].value

            left_index  = start_index
            right_index = end_index

            while True:
                ## draw start and end
                self.draw_area(start_index, end_index, pivot)

                ## find a value bigger than the pivot
                ## from the left side
                self.draw((left_index, 'Blue'))
                self.sleep()
                while dataset[left_index] < pivot:
                    self.reset_colors(left_index)

                    left_index += 1

                    self.draw_area(start_index, end_index, pivot)
                    self.draw((left_index, 'Blue'))
                    self.sleep()


                ## find a value smaller than the pivot
                ## from the right side
                self.draw((right_index, 'Pink'))
                self.sleep()
                while pivot < dataset[right_index]:
                    self.reset_colors(right_index)

                    right_index -= 1

                    self.draw_area(start_index, end_index, pivot)
                    self.draw((right_index, 'Pink'))
                    self.sleep()


                if right_index <= left_index:
                    ## reset colors after that break
                    self.reset_colors(left_index, right_index
                                      , get_pivot_index(start_index, end_index), self.get_current_pivot_index(pivot))
                    break

                ## draw objects
                self.draw((left_index, 'Red'), (right_index, 'Red'))
                self.sleep()

                ## swap each data
                self.swap(left_index, right_index)

                ## draw
                self.draw((left_index, 'Red'), (right_index, 'Red'))
                self.sleep()

                ## reset colors
                self.reset_colors(left_index, right_index)

                left_index  += 1
                right_index -= 1

            ## reset colors
            self.reset_colors(start_index, end_index)

            if start_index < left_index - 1:
                __recursive(start_index=start_index, end_index=(left_index - 1))

            if right_index + 1 < end_index:
                __recursive(start_index=(right_index + 1), end_index=end_index)

        __recursive(0, len(dataset)-1)

        ## draw all objects
        self.draw_all('Yellow')

