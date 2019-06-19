#!/usr/bin/env python3
# 

import os, sys, re, json, numpy as np

import time

from urllib.request import urlopen, Request as urlrequest
from urllib.parse import urlencode
from urllib.error import HTTPError

from xml.etree import ElementTree as xmltree

from xml.dom import minidom

import xmltodict  # sudo pip intall xmltodict

from pprint import pprint

from wordcloud import WordCloud

import matplotlib.pyplot as plt

from astropy.table import Table

from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS




def get_word_filters(
        include_prepositions = True, 
        include_conjunctions = True, 
        include_articles = True):
    # 
    word_filters = []
    # 
    if include_prepositions:
        word_filters.extend( [ 
                        'with', 
                        'at', 
                        'from', 
                        'into', 
                        'during', 
                        'including', 
                        'until', 
                        'against', 
                        'among', 
                        'throughout', 
                        'despite', 
                        'towards', 
                        'upon', 
                        'concerning', 
                        'of', 
                        'to', 
                        'in', 
                        'for', 
                        'on', 
                        'by', 
                        'about', 
                        'like', 
                        'through', 
                        'over', 
                        'before', 
                        'between', 
                        'after', 
                        'since', 
                        'without', 
                        'under', 
                        'within', 
                        'along', 
                        'following', 
                        'across', 
                        'behind', 
                        'beyond', 
                        'plus', 
                        'except', 
                        'but', 
                        'up', 
                        'out', 
                        'around', 
                        'down', 
                        'off', 
                        'above', 
                        'near', 
        ] )
        # from -- https://www.talkenglish.com/vocabulary/top-50-prepositions.aspx
    # 
    if include_conjunctions:
        word_filters.extend( [ 
                        'and', 
                        'that', 
                        'but', 
                        'or', 
                        'as', 
                        'if', 
                        'when', 
                        'than', 
                        'because', 
                        'while', 
                        'where', 
                        'after', 
                        'so', 
                        'though', 
                        'since', 
                        'until', 
                        'whether', 
                        'before', 
                        'although', 
                        'nor', 
                        'like', 
                        'once', 
                        'unless', 
                        'now', 
                        'except', 
        ] )
        # from -- https://www.englishclub.com/vocabulary/common-conjunctions-25.htm
    # 
    if include_articles:
        word_filters.extend( [ 
                        'the', 
                        'a', 
                        'an', 
                        'one', 
                        'some', 
                        'few', 
        ] )
        # from -- http://mylanguages.org/english_articles.php
    # 
    if True:
        word_filters.extend( [ 
                        'when', 
                        'where', 
                        'who', 
                        'how', 
                        'are', 
                        'is', 
                        'this', 
                        'that', 
                        'these', 
                        'those', 
                        'which', 
                        'there', 
                        'here', 
                        'also', 
                        'have', 
                        'we', 
                        'our', 
                        'them', 
                        'their', 
                        'theirs', 
        ] )
        # from -- http://mylanguages.org/english_articles.php
    # 
    return word_filters



def str_replace_accents(str_parsed):
    str_parsed = re.sub(r'([a-z])\'s ', r'\1 ', str_parsed)
    str_parsed = re.sub(r'\\\'[{]?a[}]?', r'á', str_parsed) # -- Acute accent
    str_parsed = re.sub(r'\\\'[{]?Á[}]?', r'Á', str_parsed) # 
    str_parsed = re.sub(r'\\\'[{]?e[}]?', r'é', str_parsed) # 
    str_parsed = re.sub(r'\\\'[{]?E[}]?', r'É', str_parsed) # 
    str_parsed = re.sub(r'\\\'[{]?\\i[}]?', r'í', str_parsed) # 
    str_parsed = re.sub(r'\\\'[{]?\\I[}]?', r'Í', str_parsed) # 
    str_parsed = re.sub(r'\\\'[{]?o[}]?', r'ó', str_parsed) # 
    str_parsed = re.sub(r'\\\'[{]?O[}]?', r'Ó', str_parsed) # 
    str_parsed = re.sub(r'\\\'[{]?u[}]?', r'ü', str_parsed) # 
    str_parsed = re.sub(r'\\\'[{]?U[}]?', r'Ü', str_parsed) # 
    str_parsed = re.sub(r'\\\'[{]?y[}]?', r'ý', str_parsed) # 
    str_parsed = re.sub(r'\\\'[{]?Y[}]?', r'Ý', str_parsed) # 
    str_parsed = re.sub(r'\\\"[{]?a[}]?', r'ä', str_parsed) # -- Umlaut or dieresis
    str_parsed = re.sub(r'\\\"[{]?Á[}]?', r'Ä', str_parsed) # 
    str_parsed = re.sub(r'\\\"[{]?e[}]?', r'ë', str_parsed) # 
    str_parsed = re.sub(r'\\\"[{]?E[}]?', r'Ë', str_parsed) # 
    str_parsed = re.sub(r'\\\"[{]?\\i[}]?', r'ï', str_parsed) # 
    str_parsed = re.sub(r'\\\"[{]?\\I[}]?', r'Ï', str_parsed) # 
    str_parsed = re.sub(r'\\\"[{]?o[}]?', r'ö', str_parsed) # 
    str_parsed = re.sub(r'\\\"[{]?O[}]?', r'Ö', str_parsed) # 
    str_parsed = re.sub(r'\\\"[{]?u[}]?', r'ü', str_parsed) # 
    str_parsed = re.sub(r'\\\"[{]?U[}]?', r'Ü', str_parsed) # 
    str_parsed = re.sub(r'\\\"[{]?y[}]?', r'ÿ', str_parsed) # 
    str_parsed = re.sub(r'\\\"[{]?Y[}]?', r'Ÿ', str_parsed) # 
    str_parsed = re.sub(r'\\\`[{]?a[}]?', r'à', str_parsed) # -- Grave accent
    str_parsed = re.sub(r'\\\`[{]?Á[}]?', r'À', str_parsed) # 
    str_parsed = re.sub(r'\\\`[{]?e[}]?', r'è', str_parsed) # 
    str_parsed = re.sub(r'\\\`[{]?E[}]?', r'È', str_parsed) # 
    str_parsed = re.sub(r'\\\`[{]?\\i[}]?', r'ì', str_parsed) # 
    str_parsed = re.sub(r'\\\`[{]?\\I[}]?', r'Ì', str_parsed) # 
    str_parsed = re.sub(r'\\\`[{]?o[}]?', r'ò', str_parsed) # 
    str_parsed = re.sub(r'\\\`[{]?O[}]?', r'Ò', str_parsed) # 
    str_parsed = re.sub(r'\\\`[{]?u[}]?', r'ù', str_parsed) # 
    str_parsed = re.sub(r'\\\`[{]?U[}]?', r'Ù', str_parsed) # 
    str_parsed = re.sub(r'\\\`[{]?y[}]?', r'ỳ', str_parsed) # 
    str_parsed = re.sub(r'\\\`[{]?Y[}]?', r'Ỳ', str_parsed) # 
    str_parsed = re.sub(r'[{]?\!\`[}]?', r'¡', str_parsed) # -- 
    str_parsed = re.sub(r'[{]?\?\`[}]?', r'¿', str_parsed) # -- https://stackoverflow.com/questions/4578912/replace-all-accented-characters-by-their-latex-equivalent
    return str_parsed


def str_replace_multiple_white_spaces(str_parsed):
    str_parsed = re.sub(r'\s+', r' ', str_parsed) # tr multiple white spaces
    return str_parsed


def str_replace_leading_and_trailing_white_spaces(str_parsed):
    str_parsed = re.sub(r'^\s+(.*)\s+$', r'\1', str_parsed) # chop leading/ending white spaces
    return str_parsed



















