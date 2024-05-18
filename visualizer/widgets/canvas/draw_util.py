# -*- coding:utf-8 -*-
# builtins
import tkinter as tk

# my-packages
from visualizer.widgets.canvas.abstract_draw_util import AbstractDrawUtil

__all__ = ['DrawUtilKeys', 'DrawUtil']

class DrawUtilKeys:
    """Draw Util's key definition Class"""
    ## for color
    DEFAULT_COLOR = 'DEFAULT_COLOR'
    CURRENT_COLOR = 'CURRENT_COLOR'

    ## for canvas's objects
    RECTANGLE     = 'RECTANGLE'
    VALUE         = 'TEXT'


class DrawUtil(AbstractDrawUtil):

    def __init__(self, rectangle_color='Green'
                 , value_color='Black'):

        ## initialize using super's initializer
        super().__init__()

        self.__default_color = {DrawUtilKeys.RECTANGLE: rectangle_color
                                , DrawUtilKeys.VALUE: value_color}

    @property
    def default_color(self):
        return self.__default_color

    @staticmethod
    def __setup_data_obj(callback):
        for key in (DrawUtilKeys.RECTANGLE, DrawUtilKeys.VALUE):
            callback(key)

    def init_dataset(self, dataset):
        """initialize dataset"""
        for data_obj in dataset:
            self.__setup_data_obj(callback=lambda key: data_obj.init_obj(key=key))

    def __get_color_util(self, data_obj, key, color):
        """get color"""
        ## default color
        if color is DrawUtilKeys.DEFAULT_COLOR:
            return self.default_color[key]
        ## current color
        elif color is DrawUtilKeys.CURRENT_COLOR:
            return data_obj.get_color(key)
        ## argument color
        else:
            return color

    @AbstractDrawUtil._canvas_checker
    def setup_dataset(self
                      , dataset, offset=(10, 4), spacing=2):
        """setup dataset"""
        if not dataset:
            return

        canvas = self.w_canvas
        offset_x, offset_y = offset

        ## update canvas widgets for using winfo_width and winfo_height
        canvas.update()

        ## setup width and height
        x_width  = (canvas.winfo_width() - offset_x) / (len(dataset))
        y_height = canvas.winfo_height() - offset_y

        ## normalizing data for rescaling real-valued numeric data within the
        ## given range
        normalized_data = [d.value / max([d.value for d in dataset])
                           for d in dataset]

        ## define an inner callback function
        def callback(key, obj, p, o, s):
            obj.set_color(key, self.__get_color_util(obj, key, DrawUtilKeys.DEFAULT_COLOR))
            obj.pos = p
            obj.offset = o
            obj.size = s

        for i, height in enumerate(normalized_data):
            ## setup x1 and x2
            x1 = (i * x_width) + (offset_x / 2)
            x2 = ((i+1) * x_width) + (offset_x / 2) - spacing

            ## setup y1 and y2
            y1 = y_height
            y2 = y_height - height * (y_height - offset_y)

            ## setup each data object
            self.__setup_data_obj(lambda key: callback(key
                                                       , dataset[i]
                                                       , p=[(x1, x2), (y1, y2)]
                                                       , o=((offset_x/2), offset_y)
                                                       , s=(x_width, y_height)))


        ## delete the callback function
        del callback

    @AbstractDrawUtil._canvas_checker
    def draw_rectangle(self, data_obj, color):
        """create rectangle"""
        key = DrawUtilKeys.RECTANGLE
        canvas = self.w_canvas
        color = self.__get_color_util(data_obj=data_obj, key=key, color=color)

        ## get data from dataset
        x1, x2 = data_obj.pos[0]
        y1, y2 = data_obj.pos[1]

        ## erase a rectangle if already existing
        self.erase_rectangle(data_obj)

        ## create a rectangle
        rectangle_obj = canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        ## set the rectangle object into the data_obj
        data_obj.set_obj(key, rectangle_obj)
        data_obj.set_color(key, color)

    @AbstractDrawUtil._canvas_checker
    def erase_rectangle(self, data_obj):
        """erase rectangle"""
        return self.w_canvas.delete(data_obj.get_obj(DrawUtilKeys.RECTANGLE))

    @AbstractDrawUtil._canvas_checker
    def draw_value(self, data_obj, color):
        """draw a value"""
        key = DrawUtilKeys.VALUE

        canvas = self.w_canvas
        color = self.__get_color_util(data_obj=data_obj, key=key, color=color)

        ## get data from dataset
        data               = data_obj.value
        x1, x2             = data_obj.pos[0]
        offset_x, offset_y = data_obj.offset
        width, height      = data_obj.size

        x = x2 - ((width - offset_x) / 2)
        y = height - offset_y

        ## create text object
        self.erase_value(data_obj)
        text_obj = canvas.create_text(x, y
                                      , anchor=tk.SE
                                      , text=str(data), fill=color)

        ## set the text object into the data_obj
        data_obj.set_obj(key, text_obj)
        data_obj.set_color(key, color)

    @AbstractDrawUtil._canvas_checker
    def erase_value(self, data_obj):
        """erase a value"""
        return self.w_canvas.delete(data_obj.get_obj(DrawUtilKeys.VALUE))

    def swap(self
             , obj_1, obj_2
             , before_callback=lambda: None
             , after_callback=lambda: None):
        """swap each data obj"""
        ## execute the before callbacks
        before_callback()

        ## swap each value
        obj_1.value, obj_2.value = obj_2.value, obj_1.value

        ## swap each height
        ## pos[1] = (y1, y2)
        obj_1.pos[1], obj_2.pos[1] = obj_2.pos[1], obj_1.pos[1]

        ## execute the after callbacks
        after_callback()


    def get_draw_function(self, dataset, show_value_flag):
        """get draw function"""
        def draw(*args):
            """draw objects by index
            necessary arguments are 'index' and 'rectangle_color'

            args=((i1, rectangle_color1, value_color1)
                  , (i2, rectangle_color2)
                  , ...)

            Examples:
                draw((0, 'Green', 'Black'), (2, 'Pink'))
            """
            for arg in args:
                index, colors = arg[0], arg[1:]
                data_obj = dataset[index]

                ## erase an obj at first
                self.erase_obj(data_obj=data_obj)

                ## draw a rectangle
                rectangle_color = self.__get_color_util(data_obj=data_obj
                                                        , key=DrawUtilKeys.RECTANGLE, color=colors[0])

                self.draw_rectangle(data_obj=data_obj
                                    , color=self.__get_color_util(data_obj=data_obj
                                                                  , key=DrawUtilKeys.RECTANGLE
                                                                  , color=rectangle_color))
                ## draw a value
                if show_value_flag:
                    ## value's color is default
                    value_colr = self.__get_color_util(data_obj=data_obj
                                                       , key=DrawUtilKeys.VALUE
                                                       , color=colors[1] if len(colors) >= 2 else DrawUtilKeys.DEFAULT_COLOR)

                    self.draw_value(data_obj=data_obj
                                    , color=self.__get_color_util(data_obj=data_obj
                                                                  , key=DrawUtilKeys.VALUE
                                                                  , color=value_colr))

        ## return the function address
        return draw


    def get_draw_all_function(self, dataset, show_value_flag):
        """get draw all function"""
        def draw_all(rectangle_color, value_color):
            ## erase all
            self.erase_all()

            ## draw objs
            for data_obj in dataset:
                self.draw_rectangle(data_obj=data_obj
                                    , color=self.__get_color_util(data_obj=data_obj
                                                                  , key=DrawUtilKeys.RECTANGLE
                                                                  , color=rectangle_color))
                if show_value_flag:
                    self.draw_value(data_obj=data_obj
                                    , color=self.__get_color_util(data_obj=data_obj
                                                                  , key=DrawUtilKeys.VALUE
                                                                  , color=value_color))

            self.w_canvas.update_idletasks()

        ## return the function address
        return draw_all

    def erase_obj(self, data_obj):
        """erase obj"""
        self.erase_rectangle(data_obj)
        self.erase_value(data_obj)

    def erase_objs(self, *data_objs):
        """erase objs"""
        for data_obj in data_objs:
            self.erase_obj(data_obj)

    def erase_all(self):
        """erase all"""
        self.w_canvas.delete(tk.ALL)