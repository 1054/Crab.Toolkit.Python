#!/usr/bin/env python3
# 

from p_import import *

#print(sys.path)

# 
# Aim this code:
# 
# (1) Fetch paper data from arxiv.org and save into local data file
# (2) Pretty data file and select only astroph.CO and astroph.GA
# 


# 
# (1) Fetch paper data from arxiv.org and save into local data file
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
date_until = '2017-12-31'
date_from = '2018-01-01'
date_until = '2018-08-14'
data_filename = 'data_%s_%s.txt'%(date_from, date_until)
pretty_data_filename = 'data_%s_%s_pretty.txt'%(date_from, date_until)
#url_base = 'http://export.arxiv.org/api/query?search_query=cat:astro-ph.CO&start=0&max_results=100&sortBy=lastUpdatedDate&sortOrder=ascending&'
url_base = 'http://export.arxiv.org/oai2?verb=ListRecords&' # see -- https://github.com/Mahdisadjadi/arxivscraper/blob/master/arxivscraper/arxivscraper.py
namespace0 = {'ns0':"http://www.openarchives.org/OAI/2.0/"}
namespace1 = {'ns1':"http://www.w3.org/2001/XMLSchema-instance"}
namespace2 = {'ns2':"http://arxiv.org/OAI/arXiv/"}
#xmltree.register_namespace('', 'http://www.w3.org/2001/XMLSchema-instance')
#xmltree.register_namespace('', 'http://www.openarchives.org/OAI/2.0/')
#xmltree.register_namespace('', 'http://arxiv.org/OAI/arXiv/')
#xmltree.register_namespace('', 'http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd')

#resumption_token = '2935580|15001'
resumption_token = ''
data_output_str = ''

if not os.path.isfile(data_filename) or resumption_token!='':
    if resumption_token!='':
        fp_mode = 'a'
        print('Opening "%s" for appending' % (data_filename))
    else:
        fp_mode = 'w'
        print('Opening "%s" for writting' % (data_filename))
    # 
    with open(data_filename, fp_mode) as fp:
        #url = 'http://export.arxiv.org/api/query?search_query=all:astroph&start=0&max_results=100'
        url_core = url_base + 'metadataPrefix=arXiv&set=physics:astro-ph&from=%s&until=%s'%(date_from, date_until) # resumptionToken=%s         root.find(OAI + 'ListRecords').find(OAI + 'resumptionToken')
        error_counter = 0
        while error_counter < 10:
            # 
            # urlopen
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
                    print(err)
                    print('Retrying after 5 seconds.')
                    time.sleep(5.0)
                    continue
                else:
                    raise
            # 
            # read response
            data_bytes = response.read()
            # 
            # parse xml and read resumption_token
            data_tree_root = xmltree.fromstring(data_bytes)
            resumption_token = ''
            for data_tree_element in data_tree_root.findall('ns0:ListRecords', namespace0):
                for sub_element in data_tree_element.findall('ns0:resumptionToken', namespace0):
                    if sub_element.text:
                        resumption_token = sub_element.text
            # 
            # write to data file
            data_pretty_str = minidom.parseString(xmltree.tostring(data_tree_root)).toprettyxml(indent='    ', encoding='UTF-8', newl='\n')
            data_pretty_str = '\n'.join([str(line,'UTF-8') for line in data_bytes.splitlines() if line.strip()]) # remove annoying multiple blank lines
            data_pretty_str = data_pretty_str + '\n' + '\n' + '\n' + '\n' + '\n'
            fp.write(data_pretty_str)
            #print(data_pretty_str)
            # 
            # append data_output_str
            #if len(data_output_str) == 0:
            #    data_output_str = data_pretty_str
            #else:
            #    data_output_str = data_output_str + '\n' + data_pretty_str
            # 
            # if no resumption_token then break
            if len(resumption_token) == 0:
                print('Finished downloading!')
                break
            else:
                time.sleep(5.0)
        
    #with open(data_filename, 'w') as fp:
    #    fp.write(data_output_str)

if not os.path.isfile(data_filename):
    print('Error! "%s" was not found!'%(data_filename))
    sys.exit()




# 
# (2) Pretty data file and select only astroph.CO and astroph.GA
# 
if not os.path.isfile(pretty_data_filename):
    print('Prettifying "%s"' % (data_filename))
    line = ''
    data_str = ''
    with open(data_filename, 'r') as fp:
        with open(pretty_data_filename, 'w') as ofp:
            fp.seek(0,2) # go to the file end.
            EOF = fp.tell() # get the end of file location
            fp.seek(0,0) # go back to file beginning
            is_first_line = True
            is_last_line = False
            while fp.tell() != EOF:
                line = fp.readline()
                if fp.tell() == EOF:
                    is_last_line = True
                if (line.startswith('<?xml') and not is_first_line) or \
                    line.startswith('<OAI-PMH') or \
                    line.startswith('</OAI-PMH') or \
                    line.startswith('<responseDate') or \
                    line.startswith('</responseDate') or \
                    line.startswith('<request') or \
                    line.startswith('</request') or \
                    line.startswith('<ListRecords') or \
                    line.startswith('</ListRecords') or \
                    line.startswith('<resumptionToken') or \
                    line.startswith('</resumptionToken'):
                    continue
                ofp.write(line)
                if is_first_line:
                    ofp.write('\n<ListRecords>\n')
                elif is_last_line:
                    ofp.write('\n</ListRecords>\n')
                is_first_line = False
                






