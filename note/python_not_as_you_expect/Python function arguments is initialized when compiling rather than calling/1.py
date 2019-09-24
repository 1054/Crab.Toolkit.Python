#!/usr/bin/env python
# 

def extendList(p_val, p_list=[]):
    p_list.append(p_val)
    return p_list

if __name__ == '__main__':
    print('run1', extendList(10))
    print('run1', extendList(123,[]))
    print('run1', extendList('a'))



