import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.metrics.pairwise import rbf_kernel
from sklearn.metrics.pairwise import cosine_similarity

class EmbedRank:
    
    def load_word_embeddings(self, words, word_embeddings):
        self.words = words
        self.X = word_embeddings # rows as words, columns as embedded features
    
    def generate_2D_example(self, examples):
        self.words = list(map(chr, range(65, 65+examples)))
        self.X = np.random.uniform(low = 0, high = 10, size = (examples,2))
    
    def plot2D(self):
        if self.X.shape[1] == 2:
            fig, ax = plt.subplots()
            ax.scatter(self.X[:,0], self.X[:,1])
            for i, txt in enumerate(self.words):
                ax.annotate(txt, (self.X[i,0],self.X[i,1]), xytext = (self.X[i,0]+0.15,self.X[i,1]-0.15))
            plt.show()

    def load_similarity_matrix(self, type = 'cosine', gamma_scale = None):
        if type == 'cosine':
            self.S = cosine_similarity(self.X)
        elif type == 'rbf':
            self.S = rbf_kernel(self.X, gamma = gamma_scale*(1/len(self.X)))
        self.S_below = np.zeros_like(self.S) # initialize threshold mask

    def threshold(self, thres = 0.2):
        self.S_below = self.S < thres
        self.S[self.S_below] = 0
    
    def load_transition_matrix(self, scale = 'softmax', tau = None):
        # TODO: Add zero threshold
        below = self.S_below.sum(axis = 1)[:, np.newaxis]
        if scale == 'softmax':
            row_sums = np.exp(self.S / tau).sum(axis = 1)[:, np.newaxis]
            row_sums_adj = row_sums - (below + np.exp(1/ tau)) # Adjust for thresholds and diagonals
            self.T = np.exp(self.S / tau) / row_sums_adj
        elif scale == 'linear':
            row_sums_adj = self.S.sum(axis = 1)[:, np.newaxis] - 1
            self.T = self.S / row_sums_adj
        to_keep = 1 - (np.eye(len(self.S)) + self.S_below)
        self.T *= to_keep
    
    def load_word_probs(self):
        G = nx.from_numpy_matrix(self.T)
        self.probs = nx.pagerank_numpy(G)
    
    def load_ranks(self):
        sort_inds = np.array(sorted(self.probs, key=self.probs.get, reverse = True))
        self.ranked = np.array(self.words)[sort_inds]
        self.ranked_labels = sort_inds.argsort()
    
    def plot_2D_with_ranks(self):
        if self.X.shape[1] == 2:
            rank_labels = [word+': '+ str(rank+1) for word,rank in zip(self.words, self.ranked_labels)]
            fig, ax = plt.subplots()
            ax.scatter(self.X[:,0], self.X[:,1])
            for i, txt in enumerate(rank_labels):
                ax.annotate(txt, (self.X[i,0],self.X[i,1]), xytext = (self.X[i,0]+0.15,self.X[i,1]-0.15))
            plt.show()

er = EmbedRank()
er.generate_2D_example(15)
er.plot2D()
er.load_similarity_matrix('rbf', gamma_scale = 0.5)
er.threshold(0.2)
er.load_transition_matrix(scale = 'linear')
er.load_word_probs()
er.load_ranks()
er.plot_2D_with_ranks()

if __name__ == '__main__':
    main()