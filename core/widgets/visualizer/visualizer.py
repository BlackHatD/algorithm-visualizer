# -*- coding:utf-8 -*-
# builtins
import functools
import tkinter as tk
from tkinter import ttk

# my-packages
from core import utils
from core.data.data_obj import DataObj
from core.widgets.visualizer.abstract_visualizer import AbstractVisualizer
from core.widgets.canvas.draw_util import DrawUtilKeys, DrawUtil
from core.algorithm.manager import AlgorithmManager


__all__ = ['Visualizer']


class Visualizer(AbstractVisualizer):
    """Visualizer Class"""

    def __init__(self
                 , win_size=(1024, 520)               # window size
                 , limit_data_size=(5, 100, 35)      # (from, to, default)
                 , limit_speed=(0.001, 1, 0.01)       # (from, to, default)
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

        ## whether displaying values, or not
        self.show_value_flag = False

        ## algorithm
        self.__current_algorithm = None
        self.__algorithm_manager = AlgorithmManager()


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

    def set_data(self, data):
        """set data"""
        self.dataset = DataObj.convert_data_to_dataset(data)


    def init(self):
        """initialize widgets"""
        self.__arrange_widgets()
        self.__setup_widgets()

        ## attach the canvas
        self.__drawer.attach(self._w_canvas)

        ## set window's position as the center
        self.set_win_center()


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

        ## register callback
        self._register_before_mainloop(lambda : self.__do_generate_dataset() if not self.dataset else None)


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
        ## combobox
        all_algorithms = self.__algorithm_manager.all_algorithm
        self._w_select_algorithm_combobox.configure(values=all_algorithms if all_algorithms else [''])
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
        ## initialize an algorithm at the first
        self.__init_algorithm()

        if self.__current_algorithm:
            ## erase all canvas's objects
            self.__drawer.erase_all()

            ## draw all canvas's objects
            self.__draw_all(DrawUtilKeys.DEFAULT_COLOR, DrawUtilKeys.DEFAULT_COLOR)

            ## set sleep timer
            self.__current_algorithm._sleep_time = self._w_speed_scale.get()
            ## start the algorithm
            self.__current_algorithm.run()


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
        show_value_flag = self.show_value_flag

        ## setup dataset
        self.__drawer.setup_dataset(self.dataset)

        ## get a function address
        draw_all = drawer.get_draw_all_function(dataset=dataset
                                                , show_value_flag=show_value_flag)

        ## execute the function
        draw_all(rectangle_color=rectangle_color, value_color=value_color)


    def register(self, *algorithms):
        """register algorithms"""
        for algorithm in algorithms:
            self.__algorithm_manager.register(algorithm)

    def __init_algorithm(self):
        """initialize an algorithm"""
        ## get an algorithm from the combobox
        selected_algorithm = self._w_select_algorithm_combobox.get()
        algorithm_obj = None

        if selected_algorithm:
            ## set a selected algorithm
            algorithm_obj = self.__algorithm_manager.get_algorithm(selected_algorithm)

            ## set the algorithm
            self.__setup_algorithm(algorithm_obj)

        ## set a selected algorithm object as a current algorithm
        self.__current_algorithm = algorithm_obj


    def __setup_algorithm(self, algorithm):
        """setup an algorithm"""
        manager = self.__algorithm_manager
        drawer  = self.__drawer
        dataset = self.dataset
        show_value_flag = self.show_value_flag

        ## setup dataset
        self.__drawer.setup_dataset(self.dataset)

        ## define functions
        draw         = drawer.get_draw_function(dataset=dataset, show_value_flag=show_value_flag)
        draw_all     = self.__draw_all

        ## attach
        manager.attach(algorithm=algorithm
                       , dataset=dataset
                       , draw=draw
                       , draw_all=draw_all
                       , swap=lambda index_1, index_2: drawer.swap(obj_1=dataset[index_1], obj_2=dataset[index_2])
                       , erase=lambda *indexes: drawer.erase_objs(*[dataset[i] for i in indexes])
                       , erase_all=lambda : drawer.erase_objs(*dataset)
                       , reset_colors=lambda *indexes: draw(*((i, DrawUtilKeys.DEFAULT_COLOR) for i in indexes))
                       , reset_color_all=lambda : draw_all(DrawUtilKeys.DEFAULT_COLOR, DrawUtilKeys.DEFAULT_COLOR)
                       )


