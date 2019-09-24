#!/usr/bin/env python
# 

class c_Parent(object):
    x = 1

class c_Child1(c_Parent):
    pass

class c_Child2(c_Parent):
    pass

if __name__ == '__main__':
    print(c_Parent.x, c_Child1.x, c_Child2.x)
    c_Child1.x = 2
    print(c_Parent.x, c_Child1.x, c_Child2.x)
    c_Parent.x = 3
    print(c_Parent.x, c_Child1.x, c_Child2.x)



