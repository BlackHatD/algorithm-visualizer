# -*- coding:utf-8 -*-
# builtins
import time
from abc import ABCMeta, abstractmethod

# my-packages
from core.data.data_obj import DataObj

__all__ = ['AbstractAlgorithm']

class AbstractAlgorithm(metaclass=ABCMeta):
    """Abstract Algorithm class"""
    def __init__(self):
        self.name    = self.__class__.__name__
        self.dataset = []

        ## belows parameter will be set when attached by manager
        self._attached        = False
        self._sleep_timer     = 0.1
        self._draw_value_flag = False

    def __call__(self, *args, **kwargs):
        """
        In an algorithm manager, an overridden class is instanced
        so if an overridden class is already instanced,
        this method is called by manager.
        """
        pass

    @abstractmethod
    def run(self):
        raise NotImplementedError()

    def get_data(self):
        """get data"""
        return DataObj.convert_dataset_to_data(dataset=self.dataset)

    def set_data(self, data):
        """convert data into dataset and it's set"""
        self.dataset = DataObj.convert_data_to_dataset(data)

    @staticmethod
    def show_data(data, _f=print):
        """"show data"""
        def __gen_text(d):
            return '|{} |'.format(
                ' |'.join([str(_d).rjust(len(str(len(d)))+1) for _d in d]))
        _f(__gen_text(data))

    def draw(self, *args):
        """
        this method will be overridden
        format is '((index1, color1), (index2, color2), ...)'
        """
        # print('| {} |'.format(' | '.join([str(self.dataset[arg[0]]) for arg in args])))

        # def p(text):
        #     print('{}:{}'.format(self.draw.__name__, text))
        # self.show_data(self.dataset, _f=p)

    def draw_all(self, color):
        """this method will be overridden"""
        print('{}:[{}]'.format(self.draw_all.__name__, ', '.join([str(d) for d in self.dataset])))

    def erase(self, *indexes):
        """this method will be overridden"""

    def erase_all(self):
        """this method will be overridden"""

    def swap(self, index_1, index_2):
        """this method will be overridden"""
        self.dataset[index_1], self.dataset[index_2] = self.dataset[index_2], self.dataset[index_1]

    def reset_color(self, *indexes):
        """this method will be overridden"""

    def reset_colors(self):
        """this method will be overridden"""

    def sleep(self):
        """sleep for drawing"""
        if self._attached:
            time.sleep(self._sleep_timer)

