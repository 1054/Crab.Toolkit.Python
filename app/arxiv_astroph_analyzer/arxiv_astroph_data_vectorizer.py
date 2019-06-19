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
if not os.path.isfile('paper_word_dict.json'):
    print('Reading "%s"' % (data_filename))
    data_tree = xmltree.parse(data_filename)
    data_tree_root = data_tree.getroot()
    #print(data_tree_root.attrib)
    #print(data_tree_root.tag)
    # data_tree_root.findall('record')
    paper_word_dict = {}
    paper_title_and_abstract_list = []
    paper_category_list = []
    record_counter = 0
    print('Counting paper_word_dict')
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
                    str_parsed = arXiv_data['title'] + '\n' + '\n' + arXiv_data['abstract'].replace('\n',' ')
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
                    str_parsed = re.sub(r'(\b[0-9.+-]+[0-9][$]?|\b[1-9][$]?)[~]?\'\'[ ,;\.]?', r'\1 arcsec ', str_parsed) # arcsec, can be: 1.2'', 1'', 23'', .2'', but not 0''
                    str_parsed = re.sub(r'(\b[0-9.+-]+[0-9][$]?|\b[1-9][$]?)[~]?\'[ ,;\.]?', r'\1 arcmin ', str_parsed) # arcmin
                    str_parsed = re.sub(r'(\b[0-9.+-]+[0-9][$]?|\b[1-9][$]?)[~]?\"[ ,;\.]?', r'\1 arcsec ', str_parsed) # arcsec
                    str_parsed = re.sub(r'\b0\"\.([0-9]+)\b', r'0.\1 arcsec ', str_parsed) # arcsec, can be 0.''4
                    str_parsed = re.sub(r'\b0\'\'\.([0-9]+)\b', r'0.\1 arcsec ', str_parsed) # arcsec, can be 0.''4
                    str_parsed = re.sub(r'\s+', r' ', str_parsed) # tr multiple white spaces
                    str_list = split_text_into_words(str_parsed)
                    for istr in range(len(str_list)):
                        str_item = str_list[istr]
                        if str_item.isdigit():
                            continue
                        if str_item.startswith(')'):
                            str_item = str_item[1:].strip() # chop first char
                        if str_item.startswith('.'):
                            str_item = str_item[1:].strip() # chop first char
                        if str_item.startswith(','):
                            str_item = str_item[1:].strip() # chop first char
                        if str_item.endswith('('):
                            str_item = str_item[0:-1].strip() # chop last char
                        if str_item.startswith('(') and not str_item.endswith(')'):
                            str_item = str_item[1:].strip() # chop first char
                        if str_item.endswith(')') and not str_item.startswith('('):
                            str_item = str_item[0:-1].strip() # chop last char
                        if str_item.strip() == '':
                            continue
                        if not (str_item in paper_word_dict):
                            paper_word_dict[str_item] = {}
                            paper_word_dict[str_item]['counter'] = 0
                            paper_word_dict[str_item]['left-word'] = {}
                            paper_word_dict[str_item]['right-word'] = {}
                        paper_word_dict[str_item]['counter'] = paper_word_dict[str_item]['counter'] + 1
                        #if str_item == 'a':
                        #    print('paper_word_dict['+str_item+'][\'counter\']++ # %d' % (paper_word_dict[str_item]['counter']))
                        if (istr-1) >= 0:
                            str_comp = str_list[istr-1]
                            if not (str_comp in paper_word_dict[str_item]['left-word']):
                                paper_word_dict[str_item]['left-word'][str_comp] = {}
                                paper_word_dict[str_item]['left-word'][str_comp]['counter'] = 0
                            paper_word_dict[str_item]['left-word'][str_comp]['counter'] = paper_word_dict[str_item]['left-word'][str_comp]['counter'] + 1
                        if (istr+1) <= len(str_list)-1:
                            str_comp = str_list[istr+1]
                            if not (str_comp in paper_word_dict[str_item]['right-word']):
                                paper_word_dict[str_item]['right-word'][str_comp] = {}
                                paper_word_dict[str_item]['right-word'][str_comp]['counter'] = 0
                            paper_word_dict[str_item]['right-word'][str_comp]['counter'] = paper_word_dict[str_item]['right-word'][str_comp]['counter'] + 1
                    #pprint(paper_word_dict)
                    # 
                    paper_title_and_abstract_list.append(str_parsed)
                    paper_category_list.append(arXiv_data['categories'])
            # 
            record_counter = record_counter + 1
            #if record_counter > 20:
            #    pprint(paper_word_dict)
            #    break
            print('Read record %d' % (record_counter))
    # 
    # write to paper_word_dict.json
    with open('paper_word_dict.json', 'w') as jfp:
        json.dump(paper_word_dict, jfp, sort_keys=True, indent=4)
        print('Written to "paper_word_dict.json"!')
    # 
    with open('paper_title_and_abstract_list.json', 'w') as ofp:
        json.dump(paper_title_and_abstract_list, ofp, sort_keys=False, indent=4)
        print('Written to "paper_title_and_abstract_list.json"!')
    # 
    with open('paper_category_list.json', 'w') as ofp:
        json.dump(paper_category_list, ofp, sort_keys=False, indent=4)
        print('Written to "paper_category_list.json"!')
# 
# purify paper_word_dict.json, 
# solving first-letter-upper-case grammar, 
# and solving end-of-sentence-period grammar, 
# 
if not os.path.isfile('paper_word_dict_purified.json'):
    print('Purifying paper_word_dict, solving first-letter-upper-case grammar ...')
    with open('paper_word_dict.json', 'r') as fp:
        paper_word_dict = json.load(fp)
        # 
        list_to_delete = []
        for str_item in paper_word_dict:
            str_pure = '' # str_pure is the pure form of the word str_item without grammar transformation, infinite?
            # solve cases like [('a','A'), ('up','Up'), ('the','The')]
            if str_item[0].isupper():
                str_pure = str_item[0].lower() + str_item[1:] # make first letter lower case
            # solve cases like [('something','something.'), ('something','something).')]
            if str_pure.endswith('.'):
                str_pure = str_pure[0:-1] # chop last char
            if str_pure.endswith(')'):
                str_pure = str_pure[0:-1] # chop last char
            #if str_item.startswith('('):
            #    str_pure = str_pure[1:]
            #if str_item.endswith('-') or str_item.endswith('–') or str_item.endswith('—'):
            #    # The three dashes are different unicode characters!
            #    str_pure = str_pure[0:-1]
            # 
            if str_pure != '':
                if str_pure in paper_word_dict:
                    print('DEBUG: Merging "%s" into "%s" counts: %d+%d=%d' % (str_item, str_pure, paper_word_dict[str_item]['counter'], paper_word_dict[str_pure]['counter'], paper_word_dict[str_item]['counter'] + paper_word_dict[str_pure]['counter']))
                    # merge word counter
                    paper_word_dict[str_pure]['counter'] = paper_word_dict[str_item]['counter'] + paper_word_dict[str_pure]['counter']
                    # also merge the 'left-word' and 'right-word' dicts by solving duplicates
                    for str_comp in paper_word_dict[str_item]['left-word']:
                        if str_comp in paper_word_dict[str_pure]['left-word']:
                            paper_word_dict[str_pure]['left-word'][str_comp]['counter'] = paper_word_dict[str_item]['left-word'][str_comp]['counter'] + paper_word_dict[str_pure]['left-word'][str_comp]['counter']
                        else:
                            paper_word_dict[str_pure]['left-word'][str_comp] = {}
                            paper_word_dict[str_pure]['left-word'][str_comp]['counter'] = paper_word_dict[str_item]['left-word'][str_comp]['counter'] # add a new dict key
                    for str_comp in paper_word_dict[str_item]['right-word']:
                        if str_comp in paper_word_dict[str_pure]['right-word']:
                            paper_word_dict[str_pure]['right-word'][str_comp]['counter'] = paper_word_dict[str_item]['right-word'][str_comp]['counter'] + paper_word_dict[str_pure]['right-word'][str_comp]['counter']
                        else:
                            paper_word_dict[str_pure]['right-word'][str_comp] = {}
                            paper_word_dict[str_pure]['right-word'][str_comp]['counter'] = paper_word_dict[str_item]['right-word'][str_comp]['counter'] # add a new dict key
                    # 
                    list_to_delete.append(str_item)
        for str_item in list_to_delete:
            del paper_word_dict[str_item]
    # 
    # write to paper_word_dict.json
    with open('paper_word_dict_purified.json', 'w') as jfp:
        json.dump(paper_word_dict, jfp, sort_keys=True, indent=4)
        print('Written to "paper_word_dict_purified.json"!')


# 
# (2) Analyze word appearance frequency, plot word cloud and word histogram
# 
#rm paper_word_dict_purified.json paper_word_counts.json paper_word_counts_filtered.json paper_word_vector.json *_filtered.pdf
if not os.path.isfile('paper_word_vector.json'):
    with open('paper_word_dict_purified.json', 'r') as fp:
        paper_word_dict = json.load(fp)
        # 
        # paper_word_counts
        paper_word_counts = {}
        paper_word_counts['words'] = []
        paper_word_counts['counts'] = []
        for str_item in paper_word_dict:
            paper_word_counts['words'].append(str_item)
            paper_word_counts['counts'].append(paper_word_dict[str_item]['counter'])
        paper_word_counts['counts'], paper_word_counts['words'] = zip(*sorted(zip(paper_word_counts['counts'], paper_word_counts['words']), reverse=True) )
        print('Number of unique words: %d' % (len(paper_word_counts['words'])))
        print('Number of all words: %d' % (sum(paper_word_counts['counts'])))
        # 
        # write to paper_word_counts.json
        with open('paper_word_counts.json', 'w') as jfp:
            json.dump(paper_word_counts, jfp, sort_keys=False, indent=4)
            print('Written to "paper_word_counts.json"!')
        # 
        # apply word_filter
        word_filters = get_word_filters()
        paper_word_counts_filtered = {}
        paper_word_counts_filtered['words'] = []
        paper_word_counts_filtered['counts'] = []
        for i in range(len(paper_word_counts['words'])):
            str_item = paper_word_counts['words'][i]
            # filter some words
            if len(str_item) <= 1:
                continue # filter out singel character word
            elif str_item.startswith('$'):
                continue # filter out equations
            elif str_item.startswith('\"'):
                continue # filter out quotes
            elif str_item in word_filters:
                continue # filter out common English non-meaningful words
            elif str_item in ENGLISH_STOP_WORDS:
                continue # filter out English stopwords (words that can be roughly ignored in the meaning)
            elif sum(t.isdigit() for t in str_item) >= 3:
                continue # filter out those words which contain more than 3 digit numbers
            elif paper_word_counts['counts'][i] <= 10:
                continue # <TODO> filter out those words appeared less than 10 times
            else:
                paper_word_counts_filtered['words'].append(paper_word_counts['words'][i])
                paper_word_counts_filtered['counts'].append(paper_word_counts['counts'][i])
        # 
        # write to paper_word_counts_filtered.json
        with open('paper_word_counts_filtered.json', 'w') as jfp:
            json.dump(paper_word_counts_filtered, jfp, sort_keys=False, indent=4)
            print('Written to "paper_word_counts_filtered.json"!')
        # 
        # build word vector <TODO> excluding some high frequency words
        paper_word_vector = paper_word_counts_filtered['words']
        ##for i in range(len(paper_word_counts_filtered['words'])):
        ##    str_item = paper_word_counts_filtered['words'][i]
        ##    paper_word_vector.append(str_item)
        # 
        # write to paper_word_vector.json
        with open('paper_word_vector.json', 'w') as jfp:
            json.dump(paper_word_vector, jfp, sort_keys=False, indent=4)
            print('Written to "paper_word_vector.json"!')
        # 
        # delete previous figures
        if os.path.isfile('paper_word_cloud.pdf'):
            os.system('rm paper_word_cloud.pdf')
        if os.path.isfile('paper_word_cloud_filtered.pdf'):
            os.system('rm paper_word_cloud_filtered.pdf')
        if os.path.isfile('paper_word_histogram.pdf'):
            os.system('rm paper_word_histogram.pdf')
        if os.path.isfile('paper_word_histogram_filtered.pdf'):
            os.system('rm paper_word_histogram_filtered.pdf')
        if os.path.isfile('paper_word_count_histogram.pdf'):
            os.system('rm paper_word_count_histogram.pdf')
        if os.path.isfile('paper_word_count_histogram_filtered.pdf'):
            os.system('rm paper_word_count_histogram_filtered.pdf')
        # 
# 
# make wordcloud figure
for output_suffix in ['', '_filtered']:
    if not os.path.isfile('paper_word_cloud'+output_suffix+'.pdf'):
        with open('paper_word_counts'+output_suffix+'.json', 'r') as fp:
            paper_word_counts = json.load(fp)
            # 
            # plot wordcloud, see -- https://github.com/amueller/word_cloud/blob/master/wordcloud/wordcloud.py
            print('Plotting "paper_word_cloud'+output_suffix+'.pdf"')
            paper_word_counter_dict = {}
            for i in range(len(paper_word_counts['words'])):
                paper_word_counter_dict[paper_word_counts['words'][i]] = paper_word_counts['counts'][i]
            # 
            # write to paper_word_counter_dict.json
            with open('paper_word_counter_dict.json', 'w') as jfp:
                json.dump(paper_word_counter_dict, jfp, sort_keys=True, indent=4)
                print('Written to "paper_word_counter_dict.json"!')
            # 
            # plot WordCloud
            paper_word_cloud = WordCloud(width=900,height=500,max_words=1628,relative_scaling=1,normalize_plurals=False).generate_from_frequencies(paper_word_counter_dict)
            plt.imshow(paper_word_cloud, interpolation='bilinear')
            plt.axis("off")
            #plt.show()
            plt.savefig('paper_word_cloud'+output_suffix+'.pdf')
            plt.close()
# 
# make wordhistogram figure
for output_suffix in ['', '_filtered']:
    if not os.path.isfile('paper_word_histogram'+output_suffix+'.pdf'):
        with open('paper_word_counts'+output_suffix+'.json', 'r') as fp:
            paper_word_counts = json.load(fp)
            # 
            # plot histogram
            plot_values = np.array(paper_word_counts['counts'])
            plot_labels = np.array(paper_word_counts['words'])
            #plot_argsort = np.argsort(plot_values)[::-1]
            #plot_mask = plot_argsort[0:200] # <TODO> print first 120 words
            plot_mask = np.arange(250)
            plot_base = np.arange(len(plot_mask))
            #print((plot_labels[plot_mask],plot_values[plot_mask]))
            print('Plotting "paper_word_histogram'+output_suffix+'.pdf"')
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
            plt.savefig('paper_word_histogram'+output_suffix+'.pdf')
            plt.close()
# 
# make wordcounthistogram figure
for output_suffix in ['', '_filtered']:
    if not os.path.isfile('paper_word_count_histogram'+output_suffix+'.pdf'):
        with open('paper_word_counts'+output_suffix+'.json', 'r') as fp:
            paper_word_counts = json.load(fp)
            # 
            # plot histogram
            bin_hists, bin_edges = np.histogram(np.log10(np.array(paper_word_counts['counts'])), bins=np.arange(0.0,3.0,0.025))
            bin_cents = (bin_edges[0:-1] + bin_edges[1:]) / 2.0
            plot_values = bin_hists
            plot_labels = np.round(np.power(10, bin_cents), 2)
            #plot_argsort = np.argsort(plot_values)[::-1]
            #plot_mask = plot_argsort[0:200] # <TODO> print first 120 words
            #plot_mask = np.arange(200)
            #print((plot_labels[plot_mask],plot_values[plot_mask]))
            print('Plotting "paper_word_count_histogram'+output_suffix+'.pdf"')
            plt.figure(figsize=(40.0,5.0))
            plt.bar(bin_cents, plot_values, align='center')
            plt.xticks(bin_cents, plot_labels, rotation='vertical')
            plt.yscale('log')
            plt.rc('grid', linestyle="-", color='black', alpha=0.5, linewidth=0.25)
            plt.grid()
            plt.subplots_adjust(bottom=0.24, top=0.97, left=0.03, right=0.99)
            #plt.show()
            plt.savefig('paper_word_count_histogram'+output_suffix+'.pdf')
            plt.close()




# 
# (3) Vectorize each paper data with word vector by counting
# 
if not os.path.isfile('paper_data_vectorized.json'):
    with open('paper_title_and_abstract_list.json', 'r') as ifp:
        paper_title_and_abstract_list = json.load(ifp)
    with open('paper_word_vector.json', 'r') as ifp:
        paper_word_vector = json.load(ifp)
    # 
    # loop
    print('Vectorizing the whole data ...')
    print('Word vector size %d' % (len(paper_word_vector)))
    paper_data_vectorized = np.zeros( (len(paper_title_and_abstract_list), len(paper_word_vector)), dtype=int )
    for irow in range(len(paper_title_and_abstract_list)):
        str_parsed = paper_title_and_abstract_list[irow]
        str_list = split_text_into_words(str_parsed)
        vec = [str_list.count(t) for t in paper_word_vector]
        paper_data_vectorized[irow,:] = vec
        if (irow+1) % int(float(len(paper_title_and_abstract_list))/100) == 0 or (irow+1) == len(paper_title_and_abstract_list):
            print('row %d / %d (%.2f%%)' % (irow+1, len(paper_title_and_abstract_list), float(irow+1)/len(paper_title_and_abstract_list)*100.0 ) )
    # 
    # write to paper_data_vectorized.fits
    np.save('paper_data_vectorized.numpy.bin', paper_data_vectorized)
    print('Written to "paper_data_vectorized.numpy.bin"!')
    # 
    paper_data_vectorized_table = Table(paper_data_vectorized, meta={'word_vector': paper_word_vector}, dtype=[int]*len(paper_word_vector) )
    paper_data_vectorized_table.write('paper_data_vectorized.fits', format='fits')
    print('Written to "paper_data_vectorized.fits"!')


# 
# (4) Output to "data_*_pretty_vector.txt"
# 







