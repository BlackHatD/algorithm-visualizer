# -*- coding:utf-8 -*-
# my-packages
from sample_setuper import *


if __name__ == '__main__':
    ## create a sample dataset
    dataset = DataObj.convert_data_to_dataset([(i+1) for i in range(10)])
    drawer = setuper(dataset)

    ## swap data obj
    print(dataset)
    drawer.swap(dataset[0], dataset[9])
    print(dataset)
    drawer.swap(dataset[1], dataset[8])
    print(dataset)
    drawer.swap(dataset[1], dataset[9])
    print(dataset)

    ## draw rectangles
    for data_obj in dataset:
        drawer.draw_rectangle(data_obj, DrawUtilKeys.DEFAULT_COLOR)
        drawer.draw_value(data_obj, DrawUtilKeys.DEFAULT_COLOR)

    ## erase objects
    drawer.erase_rectangle(data_obj=dataset[2])

    root.mainloop()
