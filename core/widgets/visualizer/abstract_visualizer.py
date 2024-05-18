# -*- coding:utf-8 -*-
# builtins
import copy
import functools
import threading
import tkinter as tk
from abc import ABCMeta, abstractmethod

# my-packages
from core import utils

__all__ = ['AbstractVisualizer']


class AbstractVisualizer(metaclass=ABCMeta):
    """AbstractVisualizer"""

    def __init__(self, win_size):
        ## for killing the thread id
        self.__threads = {}

        ## before mainloop
        self.__before_callback = []

        ##======================================================================##
        ## root
        self._w_root = tk.Tk()
        self._w_width, self._w_height = win_size

        ### a flag whether the window's pos is centered, or not
        self.__win_center_flag = False

        ### set a title and window size
        self.set_title(self.__class__.__name__)
        self.set_win_size(self._w_width, self._w_height)

        ##======================================================================##
        ## root frame
        ##======================================================================##
        self._w_roo_frame = tk.Frame(self._w_root)
        self._w_roo_frame.pack(fill=tk.BOTH, expand=True)

        ##======================================================================##
        ## top frame
        ##======================================================================##
        self._w_top_frame = tk.Frame(self._w_roo_frame)
        self._w_top_frame.pack(side=tk.TOP, fill=tk.X)

        ##======================================================================##
        ## bottom frame
        ##======================================================================##
        self._w_bottom_frame = tk.Frame(self._w_roo_frame)
        self._w_bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        ##======================================================================##
        ## left frame
        ##======================================================================##
        self._w_left_frame = tk.Frame(self._w_roo_frame)
        self._w_left_frame.pack(side=tk.LEFT, fill=tk.Y)

        ##======================================================================##
        ## right frame
        ##======================================================================##
        self._w_right_frame = tk.Frame(self._w_roo_frame)
        self._w_right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        ##======================================================================##
        ## main frame
        ##======================================================================##
        self._w_main_frame = tk.Frame(self._w_roo_frame)
        self._w_main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    @abstractmethod
    def init(self):
        """an initialization method, which will be overridden"""
        raise NotImplementedError()

    @property
    def _threads(self):
        return self.__threads

    @_threads.setter
    def _threads(self, thread_id):
        self.__threads[thread_id] = thread_id

    @staticmethod
    def _do_run_as_thread_decorator(m):
        @functools.wraps(m)
        def wrapper(self, *args, **kwargs):
            def callback():
                self._threads = threading.current_thread().native_id
                return m(self, *args, **kwargs)
            threading.Thread(target=callback).start()
        return wrapper

    def _register_before_mainloop(self, callback):
        """register a callback, it's run before mainloop"""
        self.__before_callback.append(callback)

    def set_title(self, title):
        """set the title"""
        self._w_root.title(title)

    def set_win_size(self, width=0, height=0):
        """set the window size"""
        self._w_width  = width  if width != 0 else self._w_width
        self._w_height = height if height != 0 else self._w_height
        self._w_root.geometry('{}x{}'.format(self._w_width, self._w_height))

    def set_win_center(self):
        """only set the center flag"""
        self.__win_center_flag = True

    def __set_win_center(self):
        """set the window at the center"""
        ## screen size
        sw, sh = utils.get_screen_size()

        ## application size
        aw = self._w_width
        ah = self._w_height

        x = (sw // 2) - (aw // 2)  # (screen width  / 2) - (application width  / 2)
        y = (sh // 2) - (ah // 2)  # (screen height / 2) - (application height / 2)

        self._w_root.geometry('+{x}+{y}'.format(x=x, y=y))

    @staticmethod
    def _toggle_widget_state(w, state_a, state_b):
        """toggle widget state"""
        current_state = str(w['state'])
        state = state_b if current_state == state_a else state_a
        return w.configure(state=state)

    def _kill_thread(self, thread_id):
        """kill thread"""
        thread_id = self._threads.pop(thread_id, None)
        if thread_id:
            return utils.kill_thread(thread_id)

    def _kill_all_threads(self):
        """kill all threads"""
        for thread_id in copy.deepcopy(self._threads).keys():
            self._kill_thread(thread_id)

    def _closer(self):
        """when push the close button, this method is run"""
        self._kill_all_threads()
        ## destroy the root widget
        self._w_root.destroy()

    def mainloop(self):
        """main loop"""
        ## set closer
        self._w_root.protocol('WM_DELETE_WINDOW', self._closer)

        ## move the window pos to center
        if self.__win_center_flag:
            self.__set_win_center()

        ## execute the callbacks
        for callback in self.__before_callback:
            callback()

        return self._w_root.mainloop()
