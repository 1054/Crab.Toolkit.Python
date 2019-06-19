#!/bin/bash
# 

python setup_lib_test_1.py build_ext --inplace -f

#clang -L/usr/lib -lstdc++ -L/opt/local/Library/Frameworks/Python.framework/Versions/3.6/lib -lpython3.6 -shared build/temp.macosx-10.12-x86_64-3.6/lib_test_1.o -o lib_test_1.so

