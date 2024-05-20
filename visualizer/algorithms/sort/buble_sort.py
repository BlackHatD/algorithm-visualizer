# -*- coding:utf-8 -*-

# my-packages
from visualizer.core.algorithm import AbstractAlgorithm

__all__ = ['BubbleSort']

class BubbleSort(AbstractAlgorithm):
    """Bubble Sort"""

    def run(self):
        dataset = self.dataset
        n = len(dataset)

        for i in range(n):

            for j in range(0, ((n-i)-1)):
                ## draw
                self.draw((j, 'Blue'), (j+1, 'Pink'))
                self.sleep()

                ## sort
                if dataset[j] > dataset[j+1]:
                    ## swap data
                    self.swap(j, j+1)

                    ## draw
                    self.draw((j, 'Red'), (j+1, 'Red'))
                    self.sleep()

                ## reset colors
                self.reset_colors(j, j + 1)

        # draw all objects
        self.draw_all('Yellow')


