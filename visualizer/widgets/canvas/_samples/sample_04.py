# -*- coding:utf-8 -*-
# my-packages
from sample_setuper import *

if __name__ == '__main__':
    ## create a sample dataset
    dataset = DataObj.convert_data_to_dataset([(i+1) for i in range(10)])
    drawer = setuper(dataset)

    draw_all = drawer.get_draw_all_function(dataset=dataset, show_value_flag=True)
    draw_all('Blue', 'White')

    drawer.erase_obj(data_obj=dataset[4])
    drawer.erase_objs(dataset[0], dataset[9])

    root.mainloop()
