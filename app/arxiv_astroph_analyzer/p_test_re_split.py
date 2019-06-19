#!/usr/bin/env python3
# 
import re

regex_splitter = re.compile(r'(\s+|\".*?\"|\'.*?\'|\$.*?\$)')

str_parsed = 'asdfasdfsadf asdf asdf adsf "bb cccccc" \'aa bbbbbbb\' ' + r'$\math abcd = 123 + 456 ^789 \text $'
print(str_parsed)

print(regex_splitter.split(str_parsed))

str_list = [t for t in regex_splitter.split(str_parsed) if t.strip()] # this can prevent from including pure white space element
print(str_list)
print(str_list[-1])
