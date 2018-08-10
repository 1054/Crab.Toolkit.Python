#!/usr/bin/env python3.6
# 

import os, sys, re, json

import time

from urllib.request import urlopen, Request as urlrequest
from urllib.parse import urlencode
from urllib.error import HTTPError

from xml.etree import ElementTree as xmltree

from xml.dom import minidom


