#!/usr/bin/env python3.6
# 

from p_import import *

#print(sys.path)

# 
# Subroutine of this code:
# (1) Fetch papers from "https://arxiv.org/list?year=18&month=all&archive=astro-ph&submit=Go"
# (2) Convert paper titles and abstracts into word vectors
# (3) Use Machine Learning to sort papers into pre-defined scientific categories
# 

# 
# (1) Fecth papers
#   Arxiv API: https://arxiv.org/help/api/index
#     API calls are made via an HTTP GET or POST requests to an appropriate url. For example, the url
#     http://export.arxiv.org/api/query?search_query=all:electron
#     A Python Example:
#       import urllib
#       url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1'
#       data = urllib.urlopen(url).read()
#       print data
#     Some notes:
#       In cases where the API needs to be called multiple times in a row, we encourage you to play nice and incorporate a 3 second delay in your code. The detailed examples below illustrate how to do this in a variety of languages.
#       Because of speed limitations in our implementation of the API, the maximum number of results returned from a single call (max_results) is limited to 30000 in slices of at most 2000 at a time, using the max_results and start query parameters. For example to retrieve matches 6001-8000:
#       http://export.arxiv.org/api/query?search_query=all:electron&start=6000&max_results=8000
#   Arxiv Open Archives Initiative (OAI) API: https://arxiv.org/help/oa/index
#     This is an alternative API which can select date range
# 


date_from = '2017-01-01'
date_until = '2017-01-31'
data_filename = 'data_%s_%s.txt'%(date_from, date_until)
#url_base = 'http://export.arxiv.org/api/query?search_query=cat:astro-ph.CO&start=0&max_results=100&sortBy=lastUpdatedDate&sortOrder=ascending&'
url_base = 'http://export.arxiv.org/oai2?verb=ListRecords&' # see -- https://github.com/Mahdisadjadi/arxivscraper/blob/master/arxivscraper/arxivscraper.py
namespace0 = {'ns0':"http://www.openarchives.org/OAI/2.0/"}
namespace1 = {'ns1':"http://www.w3.org/2001/XMLSchema-instance"}
namespace1 = {'ns2':"http://arxiv.org/OAI/arXiv/"}


if not os.path.isfile(data_filename):
    #url = 'http://export.arxiv.org/api/query?search_query=all:astroph&start=0&max_results=100'
    url_core = url_base + 'metadataPrefix=arXiv&set=physics:astro-ph&from=%s&until=%s'%(date_from, date_until) # resumptionToken=%s         root.find(OAI + 'ListRecords').find(OAI + 'resumptionToken')
    error_counter = 0
    resumption_token = ''
    data_output_str = ''
    while error_counter < 10:
        if len(resumption_token) == 0:
            url = url_core
        else:
            url = url_base + 'resumptionToken=%s'%(resumption_token) # note that here is url_base
        # 
        try:
            print('url = "%s"'%(url))
            response = urlopen(url)
        except HTTPError as err:
            if err.code == 503:
                print('Retrying after 3 seconds.')
                time.sleep(3.0)
                continue
            else:
                raise
        # 
        data_bytes = response.read()
        # 
        #xmltree.register_namespace('', 'http://www.w3.org/2001/XMLSchema-instance')
        #xmltree.register_namespace('', 'http://www.openarchives.org/OAI/2.0/')
        #xmltree.register_namespace('', 'http://arxiv.org/OAI/arXiv/')
        #xmltree.register_namespace('', 'http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd')
        data_tree_root = xmltree.fromstring(data_bytes)
        # 
        # 
        resumption_token = ''
        for data_tree_element in data_tree_root.findall('ns0:ListRecords', namespace0):
            #print(data_tree_element)
            for sub_element in data_tree_element.findall('ns0:resumptionToken', namespace0):
                #print(sub_element)
                #print(sub_element.attrib)
                #print(sub_element.text)
                if sub_element.text:
                    resumption_token = sub_element.text
        # 
        data_pretty_str = minidom.parseString(xmltree.tostring(data_tree_root)).toprettyxml(indent='    ', encoding='UTF-8', newl='\n')
        #for line in data_pretty_str.splitlines():
        #    if line.strip():
        #        print(line)
        data_pretty_str = '\n'.join([str(line,'UTF-8') for line in data_pretty_str.splitlines() if line.strip()]) # remove annoying multiple blank lines
        #print(data_pretty_str)
        # 
        if len(data_output_str) == 0:
            data_output_str = data_pretty_str
        else:
            data_output_str = data_output_str + '\n' + data_pretty_str
        # 
        if len(resumption_token) == 0:
            break
    
    with open(data_filename, 'w') as fp:
        fp.write(data_output_str)

if not os.path.isfile(data_filename):
    print('Error! "%s" was not found!'%(data_filename))
    sys.exit()




# 
# (2) Analyze papers
# 
data_tree_root = xmltree.parse(data_filename)
#print(data_tree_root.getroot().attrib)
#print(data_tree_root.getroot().tag)





