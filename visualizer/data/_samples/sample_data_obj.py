# -*- coding:utf-8 -*-
# my-packages
from visualizer.data import DataObj


if __name__ == '__main__':
    v1 = 1
    v2 = 20
    data_obj_1 = DataObj(v1)
    data_obj_2 = DataObj(v2)
    print(data_obj_1 + data_obj_2)

    data = [(i+1) for i in range(10)]
    dataset = DataObj.convert_data_to_dataset(data)
    print(dataset)

    key_obj001 = "OBJ001"
    key_obj002 = "OBJ002"
    data_obj_1.init_obj(key_obj001)
    data_obj_1.init_obj(key_obj002)
    print(data_obj_1.get_obj_details())

    data_obj_1.set_obj(key_obj001, int)
    data_obj_1.set_obj(key_obj002, str)

    data_obj_1.set_color(key_obj001, 'Green')
    data_obj_1.offset = (100, 200)
    data_obj_1.pos = ((1, 2), (3, 4))
    data_obj_1.size = (640, 480)

    print(data_obj_1.get_obj_detail(key_obj001))

    data_obj_1.clear(key_obj001)
    print(data_obj_1.get_obj_details())

    data_obj_1.clear_all()
    print(data_obj_1.get_obj_details())
