from EmbedRank import EmbedRank
import numpy as np
from numpy.random import choice

class GridSearch:

    def __init__(self):
        self.grid = {
            'similarity': ['cosine', 'rbf'],
            'gamma': np.linspace(0,1,21),
            'threshold': np.linspace(0,0.5, 11),
            'scale': ['linear', 'softmax'],
            'tau': np.linspace(0.1, 1, 19),
            'alpha': np.linspace(0.75,1,6)
        }

    def load_json(self, path):
        self.er = EmbedRank()
        self.er.load_json(path)

    def random_selection(self):
        params = {}
        params['similarity'] = choice(self.grid['similarity'])
        if params['similarity'] == 'rbf':
            params['gamma'] = choice(self.grid['gamma'])
        else:
            params['gamma'] = None
        params['threshold'] = choice(self.grid['threshold'])
        params['scale'] = choice(self.grid['scale'])
        if params['scale'] == 'softmax':
            params['tau'] = choice(self.grid['tau'])
        else:
            params['tau'] = None
        params['alpha'] = choice(self.grid['alpha'])
        return params

    def top_n_words(
        self, n, similarity, gamma,
        threshold, scale, tau, alpha):

        if similarity == 'rbf':
            self.er.load_similarity_matrix(similarity, gamma)
        else:
            self.er.load_similarity_matrix(similarity)
        self.er.threshold(threshold)
        if scale == 'softmax':
            self.er.load_transition_matrix(scale, tau)
        else:
            self.er.load_transition_matrix(scale)
        v = self.er.pagerank(alpha)
        top_n_words = self.er.words[np.argsort(v)][:n]
        return top_n_words

    def random_grid_search(self, n_words = 100, n_iter = 50):
        results = []
        for i in range(n_iter):
            print('Selection {}'.format(i).ljust(30,'.'), end = '')
            params = self.random_selection()
            print('Done.')
            top_n_words = self.top_n_words(n_words, **params)
            params['top_n_words'] = top_n_words
            results.append(params)
        return results


'''
er = EmbedRank()
er.load_json('embeddings-freq.json')
#er.generate_2D_example(15)
#er.plot2D()
er.load_similarity_matrix('cosine')
er.threshold(0.2)
er.load_transition_matrix(scale = 'linear')
#er.load_word_probs()
#er.load_ranks()
#er.plot_2D_with_ranks()

#if __name__ == '__main__':
#    main()
'''