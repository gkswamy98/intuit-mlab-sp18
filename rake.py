# pip install rake-nltk
# python -c "import nltk; nltk.download('stopwords')"
from rake_nltk import Rake
import json

def extract_keywords(filepath):
	with open(filepath) as data_file:    
   		json_data = json.load(data_file)
   		text = ""
   		for i in range(len(json_data)):
   			text += (json_data[i]['title'] + json_data[i]['body']).lower()
   		r = Rake()
   		r.extract_keywords_from_text()
   		return r.get_ranked_phrases()

def main():
	print(extract_keywords('./personal_finance_2017.json'))


if __name__ == '__main__':
	main()