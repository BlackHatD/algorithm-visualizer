# -*- coding:utf-8 -*-
# builtins
import copy
import functools

__all__ = ['DataObjBase']

class DataObjBase:
    """Data Object Base Class"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return '{}(value={})'.format(
            DataObjBase.__name__
            , self.value
        )

    def __getitem__(self, item):
        return self.__dict__.get(item)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    @staticmethod
    def __check_instance_decorator(m):
        @functools.wraps(m)
        def wrapper(self, other, *args, **kwargs):
            if isinstance(other, DataObjBase):
                other = other.value
            return m(self, other, *args, **kwargs)
        return wrapper

    @__check_instance_decorator
    def __add__(self, other):
        return self.value + other

    @__check_instance_decorator
    def __sub__(self, other):
        return self.value - other

    @__check_instance_decorator
    def __mul__(self, other):
        return self.value * other

    @__check_instance_decorator
    def __truediv__(self, other):
        return self.value / other

    @__check_instance_decorator
    def __floordiv__(self, other):
        return self.value // other

    @__check_instance_decorator
    def __lt__(self, other):
        return self.value < other

    @__check_instance_decorator
    def __le__(self, other):
        return self.value <= other

    @__check_instance_decorator
    def __eq__(self, other):
        return self.value == other

    @__check_instance_decorator
    def __ne__(self, other):
        return self.value != other

    @__check_instance_decorator
    def __gt__(self, other):
        return self.value > other

    @__check_instance_decorator
    def __ge__(self, other):
        return self.value >= other

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memodict):
        cls = self.__class__
        result = cls.__new__(cls)
        memodict[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memodict))
        return result
