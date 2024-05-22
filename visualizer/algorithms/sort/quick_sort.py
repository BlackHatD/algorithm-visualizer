# -*- coding:utf-8 -*-
# my-packages
from visualizer.core import DrawUtilKeys
from visualizer.core.algorithm import AbstractAlgorithm

__all__ = ['QuickSort']

class QuickSort(AbstractAlgorithm):
    """QuickSort"""
    def draw_current_pivots(self, pivot_value, color):
        """draw current pivots"""
        for i in [pi for pi in range(len(self.dataset)) if self.dataset[pi] == pivot_value]:
            self.draw((i, color))

    def draw_fence_lines(self, start_index, end_index):
        """draw fence lines and pivot"""
        rectangle_color = 'Black'
        value_color     = 'White'
        self.draw((start_index, rectangle_color, value_color), (end_index, rectangle_color, value_color))

    def draw_step(self, index, color):
        """draw step"""
        self.draw((index, color), )
        self.sleep()

    def draw_swapped(self, index_1, index_2, color):
        """draw swapped indexes"""
        self.draw((index_1, color), (index_2, color))
        self.sleep()


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
                self.draw_fence_lines(start_index, end_index)
                self.draw_current_pivots(pivot, 'Yellow')

                ## find a value bigger than the pivot
                ## from the left side
                self.draw_step(left_index, 'Blue')
                while dataset[left_index] < pivot:
                    ## reset left index's color
                    self.reset_colors(left_index)

                    left_index += 1

                    ## draw objects
                    self.draw_fence_lines(start_index, end_index)
                    self.draw_step(left_index, 'Blue')

                ## draw pivots
                self.draw_current_pivots(pivot, 'Yellow')

                ## find a value smaller than the pivot
                ## from the right side
                self.draw_step(right_index, 'Pink')
                while pivot < dataset[right_index]:
                    ## reset right index's color
                    self.reset_colors(right_index)

                    right_index -= 1

                    ## draw objects
                    self.draw_fence_lines(start_index, end_index)
                    self.draw_step(right_index, 'Pink')

                ## draw pivots
                self.draw_current_pivots(pivot, 'Yellow')

                if right_index <= left_index:
                    ## reset colors after that break
                    self.reset_colors(left_index, right_index)
                    self.draw_current_pivots(pivot, DrawUtilKeys.DEFAULT_COLOR)
                    break

                ## draw objects
                self.draw_swapped(left_index, right_index, 'Red')

                ## swap each data
                self.swap(left_index, right_index)

                ## draw objects
                self.draw_swapped(left_index, right_index, 'Red')

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

