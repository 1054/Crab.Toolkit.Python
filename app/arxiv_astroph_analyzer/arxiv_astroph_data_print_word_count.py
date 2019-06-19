#!/usr/bin/env python3
# 

from p_import import *

#print(sys.path)

# 
# Aim this code:
# 
# (1) Read "paper_word_counts.json"
# (2) Print the counter of an input word
# 



# 
# Read and Print
# 
with open('paper_word_counts.json', 'r') as fp:
    paper_word_counts = json.load(fp)
    # 
    for i in range(1,len(sys.argv)):
        print('Word "%s"' % (sys.argv[i]) )
        if sys.argv[i] in paper_word_counts['words']:
            print('Word "%s" has %d counts.' % (sys.argv[i], paper_word_counts['counts'][paper_word_counts['words'].index(sys.argv[i])]) )








