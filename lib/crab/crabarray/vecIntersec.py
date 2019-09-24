#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# 
# 
# This script will calc Intersection between Vector1 and Vector2
# 
# Example:
#     execfile('/Users/dliu/Software/ipy/setup.py')
#     Vector1 = [     'dog',   'cat',   'lion', 'elephant'   ]
#     Vector2 = ['elephant', 'mouse', 'rabbit', 'hond', 'cat']
#     crabarray.vecIntersec(Vector1, Vector2)
# 
# 
# Old info:
# 
# vecIntersec:
#     Input Vector1 and calc Intersection with Reference Vector2
#     Where Boolean Vector the same dimension as Input Vector1
# 
# whereIntersec:
#     Input Vector1 and calc Intersection with Reference Vector2
#     Output Index Vector the same dimension as Input Vector1
#     Output Index Vector is the index in Vector2 if matched, 
#     -1 if not match
# 
# Last update:
#   2015-03-28 created
# 
# 
def vecIntersec(Vector1, Vector2, Verbose=True): 
    #                            *positional_parameters, **keyword_parameters):
    #                             WhetherMatched1, WhetherMatched2, 
    #                             WhereMatched1, WhereMatched2, 
    #                             WhereUnmatch1, WhereUnmatch2, 
    #                             WhereIntersec1, WhereIntersec2):
    # 
    # WhetherMatched1 is a list of boolean showing whether Item in Vector1 can be found in Vector2 (dimen(WhetherMatched1)==dimen(Vector1))
    # WhetherMatched2 is a list of boolean showing whether Item in Vector2 can be found in Vector1 (dimen(WhetherMatched2)==dimen(Vector2))
    # WhereMatched1 is a list of index showing which items in Vector1 can be found in Vector2 (dimen(WhereMatched1)<=dimen(Vector1))
    # WhereMatched2 is a list of index showing which items in Vector2 can be found in Vector1 (dimen(WhereMatched2)<=dimen(Vector2))
    # WhereUnmatch1 is a list of index showing which items in Vector1 can not be found in Vector2 (dimen(WhereUnmatch1)<=dimen(Vector1))
    # WhereUnmatch2 is a list of index showing which items in Vector2 can not be found in Vector1 (dimen(WhereUnmatch2)<=dimen(Vector2))
    # WhereIntersec1 is a list of index of the matched item in Vector2 for each item in Vector1 (dimen(WhereIntersec1)==dimen(Vector1))
    # WhereIntersec2 is a list of index of the matched item in Vector1 for each item in Vector2 (dimen(WhereIntersec2)==dimen(Vector2))
    # 
    # e.g. Vector1         = [     'dog',   'cat',   'lion', 'elephant'   ]
    #      Vector2         = ['elephant', 'mouse', 'rabbit', 'hond', 'cat']
    # then WhetherMatched1 = [         F,       T,        F,      T       ]
    #      WhetherMatched2 = [         T,       F,        F,      F,     T]
    #      WhereMatched1   = [ 1, 3 ]
    #      WhereMatched2   = [ 0, 4 ]
    #      WhereUnmatch1   = [ 0, 2 ]
    #      WhereUnmatch2   = [ 1, 2, 3 ]
    #      WhereIntersec1  = [        -1,       4,       -1,      0       ]
    #      WhereIntersec2  = [         3,      -1,       -1,     -1,     1]
    # 
    # reference: 
    # http://stackoverflow.com/questions/11483863/python-intersection-indices-numpy-array
    WhetherMatched1 = numpy.in1d(Vector1,Vector2)
    WhetherMatched2 = numpy.in1d(Vector2,Vector1)
    WhereIntersec1 = numpy.array([-1]*len(WhetherMatched1))
    WhereIntersec2 = numpy.array([-1]*len(WhetherMatched2))
    # 
    if type(Vector1) is not numpy.ndarray:
        TempVector1 = numpy.array(Vector1)
    else:
        TempVector1 = Vector1
    # 
    if type(Vector2) is not numpy.ndarray:
        TempVector2 = numpy.array(Vector2)
    else:
        TempVector2 = Vector2
    # 
    WhereMatched1 = numpy.arange(TempVector1.shape[0])[WhetherMatched1]
    WhereUnmatch1 = numpy.arange(TempVector1.shape[0])[~WhetherMatched1]
    # 
    WhereMatched2 = numpy.arange(TempVector2.shape[0])[WhetherMatched2]
    WhereUnmatch2 = numpy.arange(TempVector2.shape[0])[~WhetherMatched2]
    # 
    WhereIntersec1[WhereMatched1] = WhereMatched2
    WhereIntersec2[WhereMatched2] = WhereMatched1
    # 
    # if 'WhetherMatched1' in keyword_parameters:
    #     keyword_parameters['WhetherMatched1'] = WhetherMatched1
    # if 'WhetherMatched2' in keyword_parameters:
    #     keyword_parameters['WhetherMatched2'] = WhetherMatched2
    # 
    return {'Vector1': Vector1, 'WhetherMatched1': WhetherMatched1, 'WhereIntersec1': WhereIntersec1, 'WhereMatched1': WhereMatched1, 'WhereUnmatch1': WhereUnmatch1, 'MatchedVector1': TempVector1[WhereMatched1], 
            'Vector2': Vector2, 'WhetherMatched2': WhetherMatched2, 'WhereIntersec2': WhereIntersec2, 'WhereMatched2': WhereMatched2, 'WhereUnmatch2': WhereUnmatch2, 'MatchedVector2': TempVector2[WhereMatched2]}



try:
    import numpy
except ImportError: 
    print "Error! Could not import numpy!"

