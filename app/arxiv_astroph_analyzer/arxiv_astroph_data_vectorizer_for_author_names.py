#!/usr/bin/env python3
# 

from p_import import *

#print(sys.path)

# 
# Aim this code:
# 
# (1) Read paper data from text file
# (2) Analyze word appearance frequency and build word vector
# (3) Vectorize each paper data with word vector by counting
# (4) Output to "data_*_pretty_vector.txt"
# 


# 
# Setup
# 
data_filename = 'data_2017-01-01_2017-12-31_pretty.txt'

regex_splitter = re.compile(r'([:,]?\s+|\.\s+|\".*?\"|\`+.*?\'+|\$.*?\$)') # split by white space, or ": ", ", ", or "$...$", '"..."' 
                                                                         # -- but not by ". ". 
                                                                         # -- We will deal with this case later, 
                                                                         # -- as for the first-letter-upper-case case.

# 
# Define function to split text into words
# 
def split_text_into_words(str_parsed):
    str_list = []
    if 'regex_splitter' in globals():
        str_list = [t.strip() for t in globals()['regex_splitter'].split(str_parsed) if t.strip()]
         # str_parsed.split() # see -- https://stackoverflow.com/questions/79968/split-a-string-by-spaces-preserving-quoted-substrings-in-python
    else:
        print('Error! Global variable \'regex_splitter\' was not set!')
        sys.exit()
    return str_list




# 
# (1) Read paper data from text file and vectorize it by analyzing the word cloud
# 
if not os.path.isfile('paper_author_dict.json'):
    print('Reading "%s"' % (data_filename))
    data_tree = xmltree.parse(data_filename)
    data_tree_root = data_tree.getroot()
    #print(data_tree_root.attrib)
    #print(data_tree_root.tag)
    # data_tree_root.findall('record')
    paper_author_dict = {}
    paper_author_name_list = []
    paper_category_list = []
    record_counter = 0
    print('Counting paper_author_dict')
    for data_tree_item in data_tree_root:
        if data_tree_item.tag == 'record':
            record_header = data_tree_item.find('.//header')
            record_metadata = data_tree_item.find('.//metadata')
            for record_item in record_metadata:
                if record_item.tag.endswith('arXiv'):
                    arXiv_namespace = re.sub(r'{(.*)}arXiv', r'\1', record_item.tag)
                    xmltree.register_namespace('', arXiv_namespace)
                    arXiv_data_str = xmltree.tostring(record_item)
                    arXiv_data = json.loads(json.dumps(xmltodict.parse(arXiv_data_str)))['arXiv']
                    #print(arXiv_data_str)
                    #pprint(arXiv_data)
                    # 
                    #arXiv_data['authors']['forenames']
                    #arXiv_data['authors']['keyname']
                    #arXiv_data['categories']
                    #arXiv_data['title']
                    #arXiv_data['abstract']
                    # 
                    str_list = []
                    arXiv_author_data_lists = arXiv_data['authors']
                    #print(arXiv_author_data_lists)
                    if type(arXiv_author_data_lists) is not list:
                        arXiv_author_data_lists = [arXiv_author_data_lists]
                    for arXiv_author_data_list in arXiv_author_data_lists:
                        if type(arXiv_author_data_list) is not list:
                            arXiv_author_data_list = [arXiv_author_data_list]
                        #print(arXiv_author_data_list)
                        for arXiv_author_data in arXiv_author_data_list:
                            arXiv_author_data_dicts = arXiv_author_data['author']
                            if type(arXiv_author_data_dicts) is not list:
                                arXiv_author_data_dicts = [arXiv_author_data_dicts]
                            #print(arXiv_author_data)
                            for arXiv_author_data_dict in arXiv_author_data_dicts:
                                str_item = str_replace_accents(arXiv_author_data_dict['keyname'])
                                if 'forenames' in arXiv_author_data_dict:
                                    str_item = str_item + ', ' + str_replace_accents(arXiv_author_data_dict['forenames'])
                                str_item = str_replace_multiple_white_spaces(str_item)
                                str_item = str_replace_leading_and_trailing_white_spaces(str_item)
                                str_list.append(str_item)
                                #print(str_item)
                                if not (str_item in paper_author_dict):
                                    paper_author_dict[str_item] = {}
                                    paper_author_dict[str_item]['counter'] = 0
                                    paper_author_dict[str_item]['affiliation'] = [] # each affiliation has a date with it
                                    if 'affiliation' in arXiv_author_data_dict:
                                        affiliation_dict = {}
                                        affiliation_dict['date'] = arXiv_data['created']
                                        affiliation_dict['affiliation'] = arXiv_author_data_dict['affiliation']
                                        #print(affiliation_dict)
                                        #sys.exit()
                                        if not (affiliation_dict in paper_author_dict[str_item]['affiliation']):
                                            paper_author_dict[str_item]['affiliation'].append(affiliation_dict)
                                paper_author_dict[str_item]['counter'] = paper_author_dict[str_item]['counter'] + 1
                    #pprint(paper_author_dict)
                    #sys.exit()
                    # 
                    paper_author_name_list.append(str_list)
                    paper_category_list.append(arXiv_data['categories'])
            # 
            record_counter = record_counter + 1
            #if record_counter > 20:
            #    pprint(paper_author_dict)
            #    break
            print('Read record %d' % (record_counter))
    # 
    # write to paper_author_dict.json
    with open('paper_author_dict.json', 'w') as jfp:
        json.dump(paper_author_dict, jfp, sort_keys=True, indent=4)
        print('Written to "paper_author_dict.json"!')
    # 
    with open('paper_author_name_list.json', 'w') as ofp:
        json.dump(paper_author_name_list, ofp, sort_keys=False, indent=4)
        print('Written to "paper_author_name_list.json"!')
    # 
    with open('paper_author_category_list.json', 'w') as ofp:
        json.dump(paper_category_list, ofp, sort_keys=False, indent=4)
        print('Written to "paper_author_category_list.json"!')
# 
# purify paper_author_dict.json, 
# solving first-letter-upper-case grammar, 
# and solving end-of-sentence-period grammar, 
# 
#--# if not os.path.isfile('paper_author_dict_purified.json'):
#--#     print('Purifying paper_author_dict, solving first-letter-upper-case grammar ...')
#--#     with open('paper_author_dict.json', 'r') as fp:
#--#         paper_author_dict = json.load(fp)
#--#         # 
#--#         list_to_delete = []
#--#         for str_item in paper_author_dict:
#--#             str_pure = '' # str_pure is the pure form of the word str_item without grammar transformation, infinite?
#--#             # solve cases like [('a','A'), ('up','Up'), ('the','The')]
#--#             if str_item[0].isupper():
#--#                 str_pure = str_item[0].lower() + str_item[1:] # make first letter lower case
#--#             # solve cases like [('something','something.'), ('something','something).')]
#--#             if str_pure.endswith('.'):
#--#                 str_pure = str_pure[0:-1] # chop last char
#--#             if str_pure.endswith(')'):
#--#                 str_pure = str_pure[0:-1] # chop last char
#--#             #if str_item.startswith('('):
#--#             #    str_pure = str_pure[1:]
#--#             #if str_item.endswith('-') or str_item.endswith('–') or str_item.endswith('—'):
#--#             #    # The three dashes are different unicode characters!
#--#             #    str_pure = str_pure[0:-1]
#--#             # 
#--#             if str_pure != '':
#--#                 if str_pure in paper_author_dict:
#--#                     print('DEBUG: Merging "%s" into "%s" counts: %d+%d=%d' % (str_item, str_pure, paper_author_dict[str_item]['counter'], paper_author_dict[str_pure]['counter'], paper_author_dict[str_item]['counter'] + paper_author_dict[str_pure]['counter']))
#--#                     # merge word counter
#--#                     paper_author_dict[str_pure]['counter'] = paper_author_dict[str_item]['counter'] + paper_author_dict[str_pure]['counter']
#--#                     # also merge the 'left-word' and 'right-word' dicts by solving duplicates
#--#                     for str_comp in paper_author_dict[str_item]['left-word']:
#--#                         if str_comp in paper_author_dict[str_pure]['left-word']:
#--#                             paper_author_dict[str_pure]['left-word'][str_comp]['counter'] = paper_author_dict[str_item]['left-word'][str_comp]['counter'] + paper_author_dict[str_pure]['left-word'][str_comp]['counter']
#--#                         else:
#--#                             paper_author_dict[str_pure]['left-word'][str_comp] = {}
#--#                             paper_author_dict[str_pure]['left-word'][str_comp]['counter'] = paper_author_dict[str_item]['left-word'][str_comp]['counter'] # add a new dict key
#--#                     for str_comp in paper_author_dict[str_item]['right-word']:
#--#                         if str_comp in paper_author_dict[str_pure]['right-word']:
#--#                             paper_author_dict[str_pure]['right-word'][str_comp]['counter'] = paper_author_dict[str_item]['right-word'][str_comp]['counter'] + paper_author_dict[str_pure]['right-word'][str_comp]['counter']
#--#                         else:
#--#                             paper_author_dict[str_pure]['right-word'][str_comp] = {}
#--#                             paper_author_dict[str_pure]['right-word'][str_comp]['counter'] = paper_author_dict[str_item]['right-word'][str_comp]['counter'] # add a new dict key
#--#                     # 
#--#                     list_to_delete.append(str_item)
#--#         for str_item in list_to_delete:
#--#             del paper_author_dict[str_item]
#--#     # 
#--#     # write to paper_author_dict.json
#--#     with open('paper_author_dict_purified.json', 'w') as jfp:
#--#         json.dump(paper_author_dict, jfp, sort_keys=True, indent=4)
#--#         print('Written to "paper_author_dict_purified.json"!')


# 
# (2) Analyze word appearance frequency, plot word cloud and word histogram
# 
#rm paper_author_dict_purified.json paper_author_counts.json paper_author_counts_filtered.json paper_author_vector.json *_filtered.pdf
if not os.path.isfile('paper_author_vector.json'):
    with open('paper_author_dict.json', 'r') as fp:
        paper_author_dict = json.load(fp)
        # 
        # paper_author_counts
        paper_author_counts = {}
        paper_author_counts['words'] = []
        paper_author_counts['counts'] = []
        for str_item in paper_author_dict:
            paper_author_counts['words'].append(str_item)
            paper_author_counts['counts'].append(paper_author_dict[str_item]['counter'])
        paper_author_counts['counts'], paper_author_counts['words'] = zip(*sorted(zip(paper_author_counts['counts'], paper_author_counts['words']), reverse=True) )
        print('Number of unique words: %d' % (len(paper_author_counts['words'])))
        print('Number of all words: %d' % (sum(paper_author_counts['counts'])))
        # 
        # write to paper_author_counts.json
        with open('paper_author_counts.json', 'w') as jfp:
            json.dump(paper_author_counts, jfp, sort_keys=False, indent=4)
            print('Written to "paper_author_counts.json"!')
        # 
        # apply word_filter
        word_filters = get_word_filters()
        paper_author_counts_filtered = {}
        paper_author_counts_filtered['words'] = []
        paper_author_counts_filtered['counts'] = []
        for i in range(len(paper_author_counts['words'])):
            str_item = paper_author_counts['words'][i]
            # filter some words
            if len(str_item) <= 1:
                continue # filter out singel character word
            elif paper_author_counts['counts'][i] <= 1:
                continue # filter out one time author
            else:
                paper_author_counts_filtered['words'].append(paper_author_counts['words'][i])
                paper_author_counts_filtered['counts'].append(paper_author_counts['counts'][i])
        # 
        # write to paper_author_counts_filtered.json
        with open('paper_author_counts_filtered.json', 'w') as jfp:
            json.dump(paper_author_counts_filtered, jfp, sort_keys=False, indent=4)
            print('Written to "paper_author_counts_filtered.json"!')
        # 
        # build word vector <TODO> excluding some high frequency words
        paper_author_vector = paper_author_counts_filtered['words']
        ##for i in range(len(paper_author_counts_filtered['words'])):
        ##    str_item = paper_author_counts_filtered['words'][i]
        ##    paper_author_vector.append(str_item)
        # 
        # write to paper_author_vector.json
        with open('paper_author_vector.json', 'w') as jfp:
            json.dump(paper_author_vector, jfp, sort_keys=False, indent=4)
            print('Written to "paper_author_vector.json"!')
        # 
        # delete previous figures
        if os.path.isfile('paper_author_cloud.pdf'):
            os.system('rm paper_author_cloud.pdf')
        if os.path.isfile('paper_author_cloud_filtered.pdf'):
            os.system('rm paper_author_cloud_filtered.pdf')
        if os.path.isfile('paper_author_histogram.pdf'):
            os.system('rm paper_author_histogram.pdf')
        if os.path.isfile('paper_author_histogram_filtered.pdf'):
            os.system('rm paper_author_histogram_filtered.pdf')
        if os.path.isfile('paper_author_count_histogram.pdf'):
            os.system('rm paper_author_count_histogram.pdf')
        if os.path.isfile('paper_author_count_histogram_filtered.pdf'):
            os.system('rm paper_author_count_histogram_filtered.pdf')
        # 
# 
# make wordcloud figure
for output_suffix in ['', '_filtered']:
    if not os.path.isfile('paper_author_cloud'+output_suffix+'.pdf'):
        with open('paper_author_counts'+output_suffix+'.json', 'r') as fp:
            paper_author_counts = json.load(fp)
            # 
            # plot wordcloud, see -- https://github.com/amueller/word_cloud/blob/master/wordcloud/wordcloud.py
            print('Plotting "paper_author_cloud'+output_suffix+'.pdf"')
            paper_author_counter_dict = {}
            for i in range(len(paper_author_counts['words'])):
                paper_author_counter_dict[paper_author_counts['words'][i]] = paper_author_counts['counts'][i]
            # 
            # write to paper_author_counter_dict.json
            with open('paper_author_counter_dict.json', 'w') as jfp:
                json.dump(paper_author_counter_dict, jfp, sort_keys=True, indent=4)
                print('Written to "paper_author_counter_dict.json"!')
            # 
            # plot WordCloud
            paper_author_cloud = WordCloud(width=900,height=500,max_words=1628,relative_scaling='auto',normalize_plurals=False,min_font_size=0).generate_from_frequencies(paper_author_counter_dict)
            plt.imshow(paper_author_cloud, interpolation='bilinear')
            plt.axis("off")
            #plt.show()
            plt.savefig('paper_author_cloud'+output_suffix+'.pdf')
            plt.close()
# 
# make wordhistogram figure
for output_suffix in ['', '_filtered']:
    if not os.path.isfile('paper_author_histogram'+output_suffix+'.pdf'):
        with open('paper_author_counts'+output_suffix+'.json', 'r') as fp:
            paper_author_counts = json.load(fp)
            # 
            # plot histogram
            plot_values = np.array(paper_author_counts['counts'])
            plot_labels = np.array(paper_author_counts['words'])
            #plot_argsort = np.argsort(plot_values)[::-1]
            #plot_mask = plot_argsort[0:200] # <TODO> print first 120 words
            plot_mask = np.arange(250)
            plot_base = np.arange(len(plot_mask))
            #print((plot_labels[plot_mask],plot_values[plot_mask]))
            print('Plotting "paper_author_histogram'+output_suffix+'.pdf"')
            plt.figure(figsize=(40.0,5.0))
            plt.bar(plot_base, plot_values[plot_mask], align='center')
            plt.xticks(plot_base, plot_labels[plot_mask], rotation='vertical')
            plt.bar(plot_base, plot_values[plot_mask], align='center')
            for i in range(len(plot_base)):
                plt.text(plot_base[i], plot_values[plot_mask][i], '%0d'%(plot_values[plot_mask][i]), rotation=90, fontsize=9, ha='center', va='bottom')
            plt.yscale('log')
            plt.rc('grid', linestyle="-", color='black', alpha=0.5, linewidth=0.25)
            plt.grid()
            plt.subplots_adjust(bottom=0.24, top=0.97, left=0.03, right=0.99)
            #plt.show()
            plt.savefig('paper_author_histogram'+output_suffix+'.pdf')
            plt.close()
# 
# make wordcounthistogram figure
for output_suffix in ['', '_filtered']:
    if not os.path.isfile('paper_author_count_histogram'+output_suffix+'.pdf'):
        with open('paper_author_counts'+output_suffix+'.json', 'r') as fp:
            paper_author_counts = json.load(fp)
            # 
            # plot histogram
            bin_hists, bin_edges = np.histogram(np.log10(np.array(paper_author_counts['counts'])), bins=np.arange(0.0,3.0,0.025))
            bin_cents = (bin_edges[0:-1] + bin_edges[1:]) / 2.0
            plot_values = bin_hists
            plot_labels = np.round(np.power(10, bin_cents), 2)
            #plot_argsort = np.argsort(plot_values)[::-1]
            #plot_mask = plot_argsort[0:200] # <TODO> print first 120 words
            #plot_mask = np.arange(200)
            #print((plot_labels[plot_mask],plot_values[plot_mask]))
            print('Plotting "paper_author_count_histogram'+output_suffix+'.pdf"')
            plt.figure(figsize=(40.0,5.0))
            plt.bar(bin_cents, plot_values, align='center')
            plt.xticks(bin_cents, plot_labels, rotation='vertical')
            plt.yscale('log')
            plt.rc('grid', linestyle="-", color='black', alpha=0.5, linewidth=0.25)
            plt.grid()
            plt.subplots_adjust(bottom=0.24, top=0.97, left=0.03, right=0.99)
            #plt.show()
            plt.savefig('paper_author_count_histogram'+output_suffix+'.pdf')
            plt.close()






# 
# (3) Vectorize each paper data with word vector by counting
# 
if not os.path.isfile('paper_data_vectorized_by_authors.json'):
    with open('paper_author_name_list.json', 'r') as ifp:
        paper_author_name_list = json.load(ifp)
    with open('paper_author_vector.json', 'r') as ifp:
        paper_author_vector = json.load(ifp)
    # 
    # loop
    print('Vectorizing the whole data ...')
    print('Word vector size %d' % (len(paper_author_vector)))
    paper_data_vectorized = np.zeros( (len(paper_author_name_list), len(paper_author_vector)), dtype=int )
    for irow in range(len(paper_author_name_list)):
        str_parsed = paper_author_name_list[irow]
        str_list = split_text_into_words(str_parsed)
        vec = [str_list.count(t) for t in paper_author_vector]
        paper_data_vectorized[irow,:] = vec
        if (irow+1) % int(float(len(paper_author_name_list))/100) == 0 or (irow+1) == len(paper_author_name_list):
            print('row %d / %d (%.2f%%)' % (irow+1, len(paper_author_name_list), float(irow+1)/len(paper_author_name_list)*100.0 ) )
    # 
    # write to paper_data_vectorized.fits
    np.save('paper_data_vectorized_by_authors.npy', paper_data_vectorized)
    print('Written to "paper_data_vectorized_by_authors.npy"!')
    # 
    #paper_data_vectorized_table = Table(paper_data_vectorized, meta={'word_vector': paper_author_vector}, dtype=[int]*len(paper_author_vector) )
    #paper_data_vectorized_table.write('paper_data_vectorized_by_authors.fits', format='fits')
    #print('Written to "paper_data_vectorized_by_authors.fits"!')


# 
# (4) Output to "data_*_pretty_vector.txt"
# 







