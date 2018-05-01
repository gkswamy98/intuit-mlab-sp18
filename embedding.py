import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
import json
import string
import random
from WordRank import WordRank
from preprocess import preprocess

import itertools
from glove import Glove, Corpus

def read_corpus(documents):
    for token in documents:
        yield token

def vectorize(documents, model_type):

    words = ['tax', 'stock', 'sales', 'income', 'debt', 'loan', 'business', 'turbotax', 'intuit', 'software', 'mouse', 'ira', 'gross', 'labtop', 'quickbooks', 'debt', 'important', 'frustrated', 'money', 'trader', 'incentive', 'restructuring', 'deflation', 'allocation', 'appraisal', 'authentication', 'benchmark', 'bankruptcy', 'payment', 'liability', 'equity', 'advance']

    if model_type.lower() == 'pca': # doc level
        pass

    elif model_type.lower() == 'tsne': # doc level
        pass

    elif model_type.lower() == 'skipgram': # word level
        model = Word2Vec(documents, size=100, sg=1)
        vocab = list(model.wv.vocab)
        # model.wv.save_word2vec_format('personal_finance.bin')
        print model_type.lower() + ' ------ '
        for word in words:
            try:
                print word + ': ' + str(model.wv.most_similar(word)[:5]) + '\n'
            except:
                print word + ' err'

    elif model_type.lower() == 'doc2vec': # doc level
        pass

    elif model_type.lower() == 'glove': # word level
        corpus = Corpus()
        corpus.fit(read_corpus(documents), window=10)

        model = Glove(no_components=100, learning_rate=0.05)
        model.fit(corpus.matrix, epochs=20, no_threads=4, verbose=True)
        model.add_dictionary(corpus.dictionary)

        print model_type.lower() + ' ------ '
        for word in words:
            print word + ': ' + str(model.most_similar(word)[:5]) + '\n'

    elif model_type.lower() == 'cbow': # word level
        model = Word2Vec(documents, sg=0)
        vocab = list(model.wv.vocab)
        # model.wv.save_word2vec_format('personal_finance.bin')
        print model_type.lower() + ' ------ '
        for word in words:
            print word + ': ' + str(model.wv.most_similar(word)[:5]) + '\n'

    return model[vocab], vocab, model

def pca(X, vocab):
    model = PCA(n_components=2)
    vecs = model.fit_transform(X)
    random.shuffle(vecs)
    size = 20
    plt.scatter(vecs[:size, 0], vecs[:size, 1])
    for i, word in enumerate(vocab):
        if i > size:
            break
        plt.annotate(word, xy=(vecs[i, 0], vecs[i, 1]))
    plt.show()

def main():
    START_YEAR = 2012
    END_YEAR = 2017
    documents = []

    with open('ratios.json') as file:
        ratios = json.load(file)
    count = 0
    for word in ratios:
        if ratios[word] > 2:
            count += 1

    for YEAR in range(START_YEAR, END_YEAR + 1):
        print YEAR
        filename = 'personal_finance_' + str(YEAR) + '.json'
        documents += preprocess(filename)

    filename = "investopedia.json"
    for i in range(4):
        documents += preprocess(filename, investopedia=True)

    filename = "quickbooks.txt"
    for i in range(2):
        documents += preprocess(filename, quickbooks=True)

    print('vectorizing')
    embeddings, vocab, model = vectorize(documents, 'skipgram')
    print len(vocab)

    # FREQ THRESHOLDING
    freq_count = {}
    for i, document in enumerate(documents):
        if i % 100:
            print(i, len(documents))
        for word in document:
            freq_count[word] = freq_count.get(word, 0) + 1

    list_dict = {}
    count = 0
    for word in vocab:
        if freq_count[word] > 20: # RAW FREQ THRESHOLDING
            if ratios.get(word, 0) > 2: # RELATIVE FREQ THRESHOLDING
                print(word)
                list_dict[word] = model[word].tolist()
                count += 1
    print(count)


    with open('reddit_embeddings.json', 'w') as file:
        json.dump(list_dict, file)

if __name__ == '__main__':
    main()


