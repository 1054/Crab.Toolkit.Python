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
# (1) Read paper data file, which is the output of "arxiv_astroph_data_downloader.py"
# 
if not os.path.isfile('str_list.txt'):
    data_filename = 'data_2017-01-01_2017-12-31_pretty.txt'
    #data_filename = 'data_test.txt'
    print('Reading "%s"' % (data_filename))
    data_tree = xmltree.parse(data_filename)
    data_tree_root = data_tree.getroot()
    #print(data_tree_root.attrib)
    #print(data_tree_root.tag)
    # data_tree_root.findall('record')
    str_list = []
    paper_title_and_abstract_list = []
    paper_category_list = []
    regex_splitter = re.compile(r'(\s+|\".*?\"|\'.*?\'|\$.*?\$)')
    record_counter = 0
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
                    str_parsed = re.sub(r'\s+', r' ', str_parsed)
                    str_list.append(str_parsed)
                    paper_title_and_abstract_list.append(str_parsed)
                    # 
                    paper_category_list.append(arXiv_data['categories'])
                    #
            record_counter = record_counter + 1
            print('Read record %d' % (record_counter))
    # write to file
    with open('str_list.txt', 'w') as fp:
        json.dump(str_list, fp, sort_keys=True, indent=4)
    with open('paper_title_and_abstract_list.txt', 'w') as fp:
        json.dump(paper_title_and_abstract_list, fp, sort_keys=True, indent=4)
    with open('paper_category_list.txt', 'w') as fp:
        json.dump(paper_category_list, fp, sort_keys=True, indent=4)
    # 
    sys.exit()

# 
# read str_list.txt and analyze it
with open('str_list.txt', 'r') as fp:
    str_list = json.load(fp)



# 
# First vectorize paragraphs
# -- https://towardsdatascience.com/machine-learning-nlp-text-classification-using-scikit-learn-python-and-nltk-c52b92a7c73a
# -- https://github.com/javedsha/text-classification/blob/master/Text%2BClassification%2Busing%2Bpython%2C%2Bscikit%2Band%2Bnltk.py
# 
from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(str_list)
print('sklearn extracted %d word features from %d string.'%(X_train_counts.shape[1], X_train_counts.shape[0]))


# 
# Then build self-organizing map
# -- http://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
#from sklearn.manifold import TSNE
#X_lower_dimension_projection = TSNE(n_components=4).fit_transform(X_train_counts.toarray())
from sklearn import cluster
k_means = cluster.KMeans(n_clusters=12)
k_means.fit(X_train_counts.toarray())


# 
# Then score term frequency (TF-IDF)
# What is TF*IDF?
# Put simply, the higher the TF*IDF score (weight), the rarer the term and vice versa. -- https://www.elephate.com/blog/what-is-tf-idf/
# TF = term frequency
# 
from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
print(X_train_tfidf.shape)













