# -*- coding:utf-8 -*-
# builtins
from abc import ABCMeta, abstractmethod

__all__ = ['AbstractDrawUtil']

class AbstractDrawUtil(metaclass=ABCMeta):
    """Abstract Draw Class"""
    def __init__(self):
        self.__w_canvas = None

    @property
    def w_canvas(self):
        return self.__w_canvas

    def attach(self, w_canvas):
        """attach a canvas widget"""
        self.__w_canvas = w_canvas
        return self

    def setup_configure(self, callback):
        """set up canvas's configure"""
        self.__w_canvas.bind('<Configure>', callback)

    @staticmethod
    def _canvas_checker(m):
        """canvas checker of decorator"""
        def wrapper(self, *args, **kwargs):
            if self.__w_canvas:
                return m(self, *args, **kwargs)
        return wrapper


    @abstractmethod
    def setup_dataset(self, dataset, offset, spacing):
        raise NotImplementedError()

    @abstractmethod
    def get_draw_function(self, dataset, show_value_flag):
        raise NotImplementedError()

    @abstractmethod
    def get_draw_all_function(self, dataset, show_value_flag):
        raise NotImplementedError()

    @abstractmethod
    def erase_obj(self, data_obj):
        raise NotImplementedError()

    @abstractmethod
    def erase_objs(self, *data_objs):
        raise NotImplementedError()

    @abstractmethod
    def erase_all(self):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def swap(dataset, index_1, index_2
             , before_callback
             , after_callback):
        raise NotImplementedError()
