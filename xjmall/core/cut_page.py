# -*- coding: utf-8 -*-

from __future__ import division

def cutpage(list1,num,size):
    num = int(num)
    size = int(size)
    return list1[(num-1)*size:num*size],int(len(list1)/size) if len(list1)%size==0 else int(len(list1)/size)+1
