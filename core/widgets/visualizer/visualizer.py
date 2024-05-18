# -*- coding:utf-8 -*-
# builtins
import functools
import tkinter as tk
from tkinter import ttk

# my-packages
from core import utils
from core.widgets.visualizer.abstract_visualizer import AbstractVisualizer
from core.widgets.canvas.draw_util import DrawUtilKeys, DrawUtil


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

    @property
    def dataset(self):
        return self.__dataset

    @dataset.setter
    def dataset(self, dataset):
        ## set a dataset
        self.__dataset = dataset
        self.__drawer.init_dataset(self.dataset)
        self.__drawer.setup_dataset(self.dataset)

    def init(self):
        """initialize widgets"""
        self.__arrange_widgets()
        self.__setup_widgets()

        ## attach the canvas
        self.__drawer.attach(self._w_canvas)

        ## set window's position as the center
        self.set_win_center()

        ## register callback
        self._register_before_mainloop(lambda : self.__do_generate_dataset())

        ## define a bind function
        def bind_draw_objs(e):
            ## delete all
            self.__drawer.w_canvas.delete(tk.ALL)

            ## draw all
            self.__draw_all(DrawUtilKeys.CURRENT_COLOR, DrawUtilKeys.CURRENT_COLOR)

            ## update
            self.__drawer.w_canvas.update_idletasks()

        ## setup callback
        self.__drawer.setup_configure(bind_draw_objs)

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
        data_size = self._w_data_size_scale.get()
        self.dataset = DataObj.convert_data_to_dataset(utils.gen_sample_data(data_size))
        self.__draw_all(DrawUtilKeys.DEFAULT_COLOR, DrawUtilKeys.DEFAULT_COLOR)

    @AbstractVisualizer._do_run_as_thread_decorator
    @__toggle_widgets_state_decorate
    def __do_start_algorithm(self):
        """start a selected algorithm"""
        import time
        while True:
            self.__do_shuffle_dataset()
            print(self.dataset)
            time.sleep(1)

    def __do_stop_algorithm(self):
        """stop the running algorithm"""
        self._kill_all_threads()
        self.__toggle_widgets_state()


    def __do_shuffle_dataset(self):
        """shuffle the dataset"""
        if self.dataset:
            self.dataset = DataObj.convert_data_to_dataset(utils.gen_sample_data(len(self.dataset)))
            self.__draw_all(DrawUtilKeys.DEFAULT_COLOR, DrawUtilKeys.DEFAULT_COLOR)

    def __draw_all(self
                   , rectangle_color=DrawUtilKeys.CURRENT_COLOR
                   , value_color=DrawUtilKeys.CURRENT_COLOR):
        """draw all"""
        drawer  = self.__drawer
        dataset = self.dataset
        show_value_flag = self.__show_value_flag

        ## setup dataset
        self.__drawer.setup_dataset(self.dataset)

        ## get a function address
        draw_all = drawer.get_draw_all_function(dataset=dataset
                                                , show_value_flag=show_value_flag)

        ## execute the function
        draw_all(rectangle_color=rectangle_color, value_color=value_color)



if __name__ == '__main__':
    from core import DataObj

    v = Visualizer()
    v.init()

    v.mainloop()
