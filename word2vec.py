import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
import json

def preprocess(filepath):
	with open(filepath) as data_file:    
   		json_data = json.load(data_file)
	documents = []
	for i in range(len(json_data)):
		text = json[i]['title'] + json[i]['body']
		tokenized = text.split(" ")
		documents.append(tokenized)
	return documents

def vectorize(documents):
	model = Word2Vec(documents)
	vocab = list(model.wv.vocab)
	model.wv.save_word2vec_format('personal_finance.bin')
	return model[vocab], vocab, model

def pca(X, vocab):
	model = PCA(n_components=2)
	vecs = model.fit_transform(X)
	plt.scatter(vecs[:, 0], vecs[:, 1])
	for i, word in enumerate(vocab):
		plt.annotate(word, xy=(vecs[i, 0], vecs[i, 1]))
	plt.show()

def main():
	docs = preprocess('./personalfinance.json')
	embedding, vocab, model = vectorize(docs)
	pca(embedding, vocab)

if __name__ == '__main__':
	main()

