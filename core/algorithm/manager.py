# -*- coding:utf-8 -*-

__all__ = ['AlgorithmManager']

class AlgorithmManager:
    """Algorithm Manager Class"""

    def __init__(self):
        self.__algorithms = {}

    @property
    def all_algorithm(self):
        return list(self.__algorithms.keys())

    def register(self, algorithm):
        """register an algorithm"""
        ## register the algorithm after generating an instance
        algorithm_obj = algorithm()
        self.__algorithms.update({algorithm_obj.name: algorithm_obj})

    def get_algorithm(self, key):
        """get an algorithm"""
        return self.__algorithms.get(key)


    @staticmethod
    def get_draw_value_flag(algorithm):
        """get draw value flag"""
        return algorithm._draw_value_flag

    @staticmethod
    def set_draw_value_flag(algorithm, flag):
        """set draw value flag"""
        algorithm._draw_value_flag = flag


    @staticmethod
    def attach(algorithm
               , dataset
               , draw, draw_all, erase, erase_all, swap
               , reset_colors, reset_color_all):
        """attach"""
        ## attach parameters
        algorithm.dataset   = dataset
        algorithm._attached = True

        ## attach methods
        algorithm.draw            = draw
        algorithm.draw_all        = draw_all
        algorithm.erase           = erase
        algorithm.erase_all       = erase_all
        algorithm.swap            = swap
        algorithm.reset_colors    = reset_colors
        algorithm.reset_color_all = reset_color_all
