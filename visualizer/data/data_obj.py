# -*- coding:utf-8 -*-
# builtins
import copy
import functools

# my-packages
from visualizer.data.base import DataObjBase

__all__ = ['DataObj']


class DataObj(DataObjBase):
    """Data Object Class for canvas widget"""
    ## private class parameters for canvas widget
    __KEY_OBJ         = 'OBJ'
    __KEY_COLOR       = 'COLOR'

    __KEY_OFFSET      = 'OFFSET'
    __KEY_POS         = 'POS'
    __KEY_SIZE        = 'SIZE'

    def __init__(self, value):
        ## initialize using super's initializer
        super().__init__(value=value)

        ## for drawing widgets
        self.__objs = {}

        self.offset = None
        self.pos    = None
        self.size   = None

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def __key_checker(m):
        """key checker of decorator"""
        @functools.wraps(m)
        def wrapper(self, key, *args, **kwargs):
            if self.__objs.get(key):
                return m(self, key, *args, **kwargs)

            raise RuntimeError(
                "[!!] The object is not initialized using %r of key. Use %r!!"
                % (key, self.init_obj.__name__)
            )

        return wrapper

    @staticmethod
    def convert_data_to_dataset(data):
        """convert data into dataset
        Examples:
            > data = [(i+1) for i in range(10)]
            > dataset = DataObj.convert_data_to_dataset(data)
        """
        return [DataObj(value=v) for v in data]

    @staticmethod
    def convert_dataset_to_data(dataset):
        """convert dataset into data"""
        return [d.value for d in dataset]

    def init_obj(self
                 , key
                 , obj=None
                 , color=None
                 , offset=(0, 0)
                 , pos=((0, 0), (0, 0))
                 , size=(0, 0)):
        """initialize an obj"""
        self.__objs.update({key: {self.__KEY_OBJ: obj
                                  , self.__KEY_COLOR: color}})
        self.offset = offset
        self.pos    = pos
        self.size   = size

    @__key_checker
    def clear(self, key):
        """clear an object"""
        self.__objs.pop(key)

    def clear_all(self):
        """clear al objects"""
        self.__objs.clear()

    @__key_checker
    def set_obj(self, key, obj):
        """set an obj"""
        self.__objs[key][self.__KEY_OBJ] = obj

    @__key_checker
    def set_color(self, key, color):
        """set an obj color"""
        self.__objs[key][self.__KEY_COLOR] = color

    @__key_checker
    def get_obj_detail(self, key):
        """get on object's details"""
        new_obj = copy.deepcopy(self.__objs[key])
        new_obj[self.__KEY_OFFSET] = self.offset
        new_obj[self.__KEY_POS]    = self.pos
        new_obj[self.__KEY_SIZE]   = self.size
        return new_obj

    def get_obj_details(self):
        """get on objects details"""
        new_objs = {}
        for key, value in copy.deepcopy(self.__objs).items():
            new_objs.update({key: self.get_obj_detail(key)})
        return new_objs

    @__key_checker
    def get_obj(self, key):
        """get object"""
        return self.__objs[key].get(self.__KEY_OBJ)

    def get_objs(self):
        """get objects"""
        return [obj[self.__KEY_OBJ] for obj in self.__objs.values()]

    @__key_checker
    def get_color(self, key):
        """get color"""
        return self.__objs[key].get(DataObj.__KEY_COLOR)
