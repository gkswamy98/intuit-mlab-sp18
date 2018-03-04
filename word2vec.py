import matplotlib.pyplot as plt
from gensim import Word2Vec
from sklearn import PCA


def vectorize(documents):
	model = Word2Vec(documents)
	vocab = list(model.wv.vocab)
	model.wv.save_word2vec_format('personal_finance.bin')
	return model[vocab], vocab

def pca(X, vocab):
	model = PCA(n_components=2)
	vecs = model.fit_transform(X)
	plt.scatter(vecs[:, 0], vecs[:, 1])
	for i, word in enumerate(vocab):
		plt.annotate(word, xy=(vecs[i, 0], vecs[i, 1]))
	plt.show()
