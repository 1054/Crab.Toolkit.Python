#!/usr/bin/env python3
# 

from p_import import *

#print(sys.path)

# 
# Aim of this code:
# (1) Read paper data file, which is the output of "arxiv_astroph_data_downloader.py"
# (2) Convert paper titles and abstracts into word vectors
# (3) Use Machine Learning to sort papers into pre-defined scientific categories
# 

# 
# (1) Read paper data file, which is the output of "arxiv_astroph_data_downloader.py", then output 'word_dict.json'
# 
if not os.path.isfile('word_dict.json'):
    data_filename = 'data_2017-01-01_2017-12-31_pretty.txt'
    data_filename = 'data_test.txt'
    print('Reading "%s"' % (data_filename))
    data_tree = xmltree.parse(data_filename)
    data_tree_root = data_tree.getroot()
    #print(data_tree_root.attrib)
    #print(data_tree_root.tag)
    # data_tree_root.findall('record')
    word_dict = {}
    regex_splitter = re.compile(r'(\s+|\".*?\"|\'.*?\'|\$.*?\$)')
    record_counter = 0
    print('Counting word_dict')
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
                    str_parsed = arXiv_data['title'] + '\n' + '\n' + arXiv_data['abstract']
                    str_list = [t for t in regex_splitter.split(str_parsed) if t.strip()] # str_parsed.split() # see -- https://stackoverflow.com/questions/79968/split-a-string-by-spaces-preserving-quoted-substrings-in-python
                    for istr in range(len(str_list)):
                        str_item = str_list[istr]
                        if str_item.isdigit():
                            continue
                        if str_item.startswith('('):
                            str_item = str_item[1:]
                        if str_item.endswith('('):
                            str_item = str_item[0:-2]
                        if not (str_item in word_dict):
                            word_dict[str_item] = {}
                            word_dict[str_item]['counter'] = 0
                            word_dict[str_item]['left-word'] = {}
                            word_dict[str_item]['right-word'] = {}
                        word_dict[str_item]['counter'] = word_dict[str_item]['counter'] + 1
                        #if str_item == 'a':
                        #    print('word_dict['+str_item+'][\'counter\']++ # %d' % (word_dict[str_item]['counter']))
                        if (istr-1) >= 0:
                            str_comp = str_list[istr-1]
                            if not (str_comp in word_dict[str_item]['left-word']):
                                word_dict[str_item]['left-word'][str_comp] = {}
                                word_dict[str_item]['left-word'][str_comp]['counter'] = 0
                            word_dict[str_item]['left-word'][str_comp]['counter'] = word_dict[str_item]['left-word'][str_comp]['counter'] + 1
                        if (istr+1) <= len(str_list)-1:
                            str_comp = str_list[istr+1]
                            if not (str_comp in word_dict[str_item]['right-word']):
                                word_dict[str_item]['right-word'][str_comp] = {}
                                word_dict[str_item]['right-word'][str_comp]['counter'] = 0
                            word_dict[str_item]['right-word'][str_comp]['counter'] = word_dict[str_item]['right-word'][str_comp]['counter'] + 1
                    #pprint(word_dict)
            record_counter = record_counter + 1
            #if record_counter > 20:
            #    pprint(word_dict)
            #    break
            print('Read record %d' % (record_counter))
    # 
    # write to word_dict.json
    with open('word_dict.json', 'w') as fp:
        json.dump(word_dict, fp, sort_keys=True, indent=4)
        print('Written to "word_dict.json"!')
# 
# purify word_dict.json
if not os.path.isfile('word_dict_purified.json'):
    with open('word_dict.json', 'r') as fp:
        word_dict = json.load(fp)
        # 
        # generate wordcloud. 
        # See documentation: https://github.com/amueller/word_cloud/blob/master/wordcloud/wordcloud.py
        list_to_delete = []
        for str_item in word_dict:
            if str_item[0].islower():
                # solve cases like [('a','A'), ('up','Up'), ('the','The')]
                str_comp = str_item[0].upper() + str_item[1:]
                if str_comp in word_dict:
                    print('DEBUG: Merging "%s" into "%s" counts: %d+%d=%d' % (str_comp, str_item, word_dict[str_comp]['counter'], word_dict[str_item]['counter'], word_dict[str_comp]['counter'] + word_dict[str_item]['counter']))
                    word_dict[str_item]['counter'] = word_dict[str_item]['counter'] + word_dict[str_comp]['counter']
                    for str_comp2 in word_dict[str_comp]['left-word']:
                        if str_comp2 in word_dict[str_item]['left-word']:
                            word_dict[str_item]['left-word'][str_comp2]['counter'] = word_dict[str_item]['left-word'][str_comp2]['counter'] + word_dict[str_comp]['left-word'][str_comp2]['counter']
                        else:
                            word_dict[str_item]['left-word'][str_comp2] = {}
                            word_dict[str_item]['left-word'][str_comp2]['counter'] = word_dict[str_comp]['left-word'][str_comp2]['counter']
                    for str_comp2 in word_dict[str_comp]['right-word']:
                        if str_comp2 in word_dict[str_item]['right-word']:
                            word_dict[str_item]['right-word'][str_comp2]['counter'] = word_dict[str_item]['right-word'][str_comp2]['counter'] + word_dict[str_comp]['right-word'][str_comp2]['counter']
                        else:
                            word_dict[str_item]['right-word'][str_comp2] = {}
                            word_dict[str_item]['right-word'][str_comp2]['counter'] = word_dict[str_comp]['right-word'][str_comp2]['counter']
                    # 
                    list_to_delete.append(str_comp)
        for str_item in list_to_delete:
            del word_dict[str_item]
        #print('Number of words: %d' % (len(word_counter)))
    # 
    # write to word_dict.json
    with open('word_dict_purified.json', 'w') as fp:
        json.dump(word_dict, fp, sort_keys=True, indent=4)
        print('Written to "word_dict_purified.json"!')
# 
# read word_dict_purified.json and plot word cloud
if not os.path.isfile('word_cloud.pdf'):
    with open('word_dict_purified.json', 'r') as fp:
        word_dict = json.load(fp)
        # 
        # generate wordcloud, see -- https://github.com/amueller/word_cloud/blob/master/wordcloud/wordcloud.py
        word_counter = {}
        for str_item in word_dict:
            word_counter[str_item] = word_dict[str_item]['counter']
        #pprint(word_counter)
        #print((word_counter.keys(),word_counter.values()))
        print('Number of words: %d' % (len(word_counter)))
        # 
        word_cloud = WordCloud(width=900,height=500, max_words=1628,relative_scaling=1,normalize_plurals=False).generate_from_frequencies(word_counter)
        plt.imshow(word_cloud, interpolation='bilinear')
        plt.axis("off")
        #plt.show()
        plt.savefig('word_cloud.pdf')
        plt.close()
        # 
        plot_values = np.array(list(word_counter.values()))
        plot_labels = np.array(list(word_counter.keys()))
        plot_mask = np.argsort(plot_values)[::-1]
        plot_mask = plot_mask[0:120]
        print((plot_labels[plot_mask],plot_values[plot_mask]))
        plt.figure(figsize=(22.0,5.0))
        plt.bar(np.arange(len(plot_mask)), plot_values[plot_mask], align='center')
        plt.xticks(np.arange(len(plot_mask)), plot_labels[plot_mask], rotation='vertical')
        plt.yscale('log')
        plt.subplots_adjust(bottom=0.24, top=0.97, left=0.03, right=0.99)
        #plt.show()
        plt.savefig('word_histogram.pdf')
        plt.close()












