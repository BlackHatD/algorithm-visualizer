# -*- coding:utf-8 -*-
# builtins
import ctypes
import random

__all__ = ['get_screen_size', 'gen_sample_data', 'kill_thread']

_user32 = ctypes.windll.user32

def get_screen_size():
    """get screen size"""
    return _user32.GetSystemMetrics(0), _user32.GetSystemMetrics(1)

def gen_sample_data(size):
    """generate random sample data"""
    return random.sample([i+1 for i in range(size)], size)


def kill_thread(thread_id):
    """kill thread"""
    return ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                      ctypes.py_object(SystemExit))

