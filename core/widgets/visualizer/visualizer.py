# -*- coding:utf-8 -*-
# builtins
import functools
import tkinter as tk
from tkinter import ttk

# my-packages
from core.widgets.visualizer.abstract_visualizer import AbstractVisualizer
from core.widgets.canvas.draw_util import DrawUtil


__all__ = ['Visualizer']


class Visualizer(AbstractVisualizer):
    """Visualizer Class"""

    def __init__(self
                 , win_size=(640, 480)               # window size
                 , limit_data_size=(5, 100, 10)      # (from, to, default)
                 , limit_speed=(0.001, 1, 0.1)       # (from, to, default)
                 , default_color=('Green', 'Black')  # (rectangle, value)
                 ):

        """initializer"""
        ##======================================================================##
        ## call super's initializer
        super().__init__(win_size=win_size)

        ## dataset
        self.__dataset = []

        ## drawer
        self.__drawer = DrawUtil(*default_color)

        # whether displaying values, or not
        self.__show_value_flag = False

        ##======================================================================##
        ## option frame
        ##======================================================================##
        self._w_option_frame = tk.LabelFrame(master=self._w_main_frame
                                             , text='Option'
                                             , padx=10, pady=10)

        ##----------------------------------------------------------------------##
        ## data scale frame
        self._w_data_scale_frame = tk.Frame(master=self._w_option_frame)

        ### create size scale widget
        data_size_scale_from, data_size_scale_to, data_size_scale_default = limit_data_size
        self._w_data_size_scale = tk. Scale(master=self._w_data_scale_frame
                                            , from_=data_size_scale_from, to=data_size_scale_to
                                            , orient=tk.HORIZONTAL, resolution=1
                                            , label='Size')

        ### set default data size
        self._w_data_size_scale.set(data_size_scale_default)

        ## create generate button widget
        self._w_generate_button = ttk.Button(master=self._w_data_scale_frame
                                             , text='GENERATE', state=tk.NORMAL)


        ##----------------------------------------------------------------------##
        ## algorithm frame
        self._w_algorithm_frame = tk.Frame(master=self._w_option_frame)

        ### create selecting algorithm combobox
        self._w_select_algorithm_combobox = ttk.Combobox(master=self._w_algorithm_frame
                                                         , state='readonly')
        ### create run button widget
        self._w_start_button = ttk.Button(master=self._w_algorithm_frame
                                          , text='START', state=tk.NORMAL)

        ### create shuffle button widget
        self._w_shuffle_button = ttk.Button(master=self._w_algorithm_frame
                                            , text='SHUFFLE', state=tk.NORMAL)

        ### create stop button widget
        self._w_stop_button = ttk.Button(master=self._w_algorithm_frame
                                         , text='STOP', state=tk.DISABLED)


        ##----------------------------------------------------------------------##
        ## speed scale frame
        self._w_speed_scale_frame = tk.Frame(master=self._w_option_frame)

        ### create speed scale widget
        ### calculate digits at first
        speed_scale_from, speed_scale_to, speed_scale_default = limit_speed
        speed_scale_from *= 1.0     # converting integer to digit
        digits = len(str(speed_scale_from).split('.')[1])

        self._w_speed_scale = tk.Scale(master=self._w_speed_scale_frame
                                       , from_=speed_scale_from, to=speed_scale_to
                                       , length=100, resolution=speed_scale_from
                                       , digits=digits+1
                                       , label='Speed')

        ### set default speed
        self._w_speed_scale.set(speed_scale_default)


        ##======================================================================##
        ## canvas frame
        ##======================================================================##
        self._w_canvas_frame = tk.LabelFrame(master=self._w_main_frame, text='Canvas')
        self._w_canvas = tk.Canvas(master=self._w_canvas_frame, background='Gray')

    def init(self):
        """initialize widgets"""
        self.__arrange_widgets()
        self.__setup_widgets()

    def __arrange_widgets(self):
        """arrange widgets"""
        ## option frame
        self._w_option_frame.pack(fill=tk.X)

        ## data scale frame
        self._w_data_scale_frame.pack(side=tk.LEFT)
        ### scale
        self._w_data_size_scale.pack(side=tk.TOP, pady='1 15')
        ### button
        self._w_generate_button.pack(side=tk.TOP)

        ## speed frame
        self._w_speed_scale_frame.pack(side=tk.RIGHT)
        self._w_speed_scale.pack(side=tk.LEFT)

        ## algorithm frame
        self._w_algorithm_frame.pack(side=tk.RIGHT)
        ### combobox
        self._w_select_algorithm_combobox.grid(row=0, column=0)

        ### button
        self._w_start_button.grid(row=0, column=1)
        self._w_shuffle_button.grid(row=1, column=1)
        self._w_stop_button.grid(row=2, column=1)

        ## canvas frame
        self._w_canvas_frame.pack(fill=tk.BOTH, expand=True)
        ### canvas
        self._w_canvas.pack(fill=tk.BOTH, expand=True)

    def __setup_widgets(self):
        """setup widgets"""
        ## TODO-#1
        ## combobox
        self._w_select_algorithm_combobox.configure(values=[''])
        self._w_select_algorithm_combobox.current(0)

        ## button
        self._w_generate_button.configure(command=self.__do_generate_dataset)
        self._w_start_button.configure(command=self.__do_start_algorithm)
        self._w_stop_button.configure(command=self.__do_stop_algorithm)
        self._w_shuffle_button.configure(command=self.__do_shuffle_dataset)

    def __toggle_widgets_state(self):
        """toggle widgets state"""
        self._toggle_widget_state(self._w_generate_button, tk.NORMAL, tk.DISABLED)
        self._toggle_widget_state(self._w_start_button, tk.NORMAL, tk.DISABLED)
        self._toggle_widget_state(self._w_stop_button, tk.NORMAL, tk.DISABLED)
        self._toggle_widget_state(self._w_shuffle_button, tk.NORMAL, tk.DISABLED)
        self._toggle_widget_state(self._w_select_algorithm_combobox, 'readonly', tk.DISABLED)

    @staticmethod
    def __toggle_widgets_state_decorate(m):
        @functools.wraps(m)
        def wrapper(self, *args, **kwargs):
            self.__toggle_widgets_state()
            ret = m(self, *args, **kwargs)
            self.__toggle_widgets_state()
            return ret
        return wrapper

    def __do_generate_dataset(self):
        """generate dataset"""
        print("[+] pushed the generate button")

    @AbstractVisualizer._do_run_as_thread_decorator
    @__toggle_widgets_state_decorate
    def __do_start_algorithm(self):
        """start a selected algorithm"""
        import datetime, time
        while True:
            print(datetime.datetime.now())
            time.sleep(1)


    def __do_stop_algorithm(self):
        """stop the running algorithm"""
        self._kill_all_threads()
        self.__toggle_widgets_state()


    def __do_shuffle_dataset(self):
        """shuffle the dataset"""
        print("[+] pushed the shuffle button")


if __name__ == '__main__':
    v = Visualizer()
    v.set_win_center()
    v.init()
    v.mainloop()
