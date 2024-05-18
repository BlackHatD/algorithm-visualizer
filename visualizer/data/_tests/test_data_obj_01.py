# -*- coding:utf-8 -*-
# my-packages
from visualizer.data import DataObj

if __name__ == '__main__':
    # Test overridden operators

    ## Define values
    v1 = 1
    v2 = 20

    ## Generate data objects from values
    d1 = DataObj(v1)
    d2 = DataObj(v2)


    ### Addition (+)
    assert (d1 + v2) == (v1 + v2), (d1 + v2)
    assert (d1 + d2) == (v1 + v2), (d1 + d2)

    ### Subtraction (-)
    assert (d1 - v2) == (v1 - v2), (d1 - v2)
    assert (d1 - d2) == (v1 - v2), (d1 - d2)

    ### Multiplication (*)
    assert (d1 * v2) == (v1 * v2), (d1 * v2)
    assert (d1 * d2) == (v1 * v2), (d1 * d2)

    ### True Division (/)
    assert (d1 / v2) == (v1 / v2), (d1 / v2)
    assert (d1 / d2) == (v1 / v2), (d1 / d2)

    ### Floor Division (//)
    assert (d1 // v2) == (v1 // v2), (d1 // v2)
    assert (d1 // d2) == (v1 // v2), (d1 // d2)

    ## Greater than (<)
    assert (d1 < v2) == (v1 < v2), (d1 < v2)
    assert (d1 < d2) == (v1 < v2), (d1 < d2)

    ## Equal to
    assert (d1 == v2) == (v1 == v2), (d1 == v2)
    assert (d1 == d2) == (v1 == v2), (d1 == d2)

    ## Less than (>)
    assert (d1 > v2) == (v1 > v2), (d1 > v2)
    assert (d1 > d2) == (v1 > v2), (d1 > d2)

