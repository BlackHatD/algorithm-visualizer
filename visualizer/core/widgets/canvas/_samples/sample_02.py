# -*- coding:utf-8 -*-
# my-packages
from sample_setuper import *

if __name__ == '__main__':
    ## create a sample dataset
    dataset = DataObj.convert_data_to_dataset([(i+1) for i in range(10)])
    drawer = setuper(dataset)

    draw = drawer.get_draw_function(dataset=dataset, show_value_flag=True)
    draw((0, 'Blue', 'Pink'), (1, 'Yellow'))
    draw((9, 'Black', 'White'), )

    root.mainloop()
