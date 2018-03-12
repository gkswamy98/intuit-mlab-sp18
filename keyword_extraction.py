# pip install rake-nltk
# python -c "import nltk; nltk.download('stopwords')"
from rake_nltk import Rake
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def get_rake_keywords(filepaths, n=10):
	freq_dict = dict()
	for filepath in filepaths:
		with open(filepath) as data_file:
			json_data = json.load(data_file)
		for i in range(len(json_data)):
			text =  json_data[i]['title'] + json_data[i]['body']
			r = Rake()
			r.extract_keywords_from_text(text)
			keywords = r.get_ranked_phrases()
			for keyword in keywords:
				if keyword in freq_dict:
					freq_dict[keyword] += 1
				else:
					freq_dict[keyword] = 1
	return sorted(freq_dict.items(), key = lambda item: item[1])[-n:]

def get_tf_idf_keywords(filepaths, n=10):
	documents = []
	for filepath in filepaths:
		with open(filepath) as data_file:
			json_data = json.load(data_file)
		for i in range(len(json_data)):
			documents.append(json_data[i]['title'] + json_data[i]['body'])
	vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1,6), min_df = 10, stop_words = 'english')
	X = vectorizer.fit_transform(documents)
	indices = np.argsort(vectorizer.idf_)[::-1]
	features = vectorizer.get_feature_names()
	top_features = [features[i] for i in indices[:n]]
	print(top_features)

def main():
	top_1k = get_tf_idf_keywords(['./personal_finance_2012.json', './personal_finance_2013.json', './personal_finance_2014.json'], 100)


if __name__ == '__main__':
	main()