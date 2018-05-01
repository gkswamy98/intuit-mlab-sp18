import json
from preprocess import preprocess_text

financial_freqs = {}
financial_count = 0

print('investopedia')
with open('investopedia.json') as file:
	data = json.load(file)
	for i, datum in enumerate(data):
		if i % 1000 == 0:
			print(i, '/', len(data))
		words = preprocess_text(datum['definition'] + ' ' + datum['break_down'])
		for word in words:
			financial_freqs[word] = financial_freqs.get(word, 0) + 5
			financial_count += 5

print('quickbooks')
with open('quickbooks.txt') as file:
	text = ""
	for line in file.readlines():
		text += line + " "
	words = preprocess_text(text)
	for word in words:
		financial_freqs[word] = financial_freqs.get(word, 0) + 5
		financial_count += 5

for YEAR in range(2012, 2017 + 1):
	file_name = 'personal_finance_' + str(YEAR) + '.json'
	print(file_name)
	with open(file_name) as file:
		data = json.load(file)
		for i, datum in enumerate(data):
			if i % 1000 == 0:
				print(i, '/', len(data))
			words = preprocess_text(datum['title'] + ' ' + datum['body'])
			for word in words:
				financial_freqs[word] = financial_freqs.get(word, 0) + 1
				financial_count += 1

freqs = {}
count = 0
for NUM in range(3, 6 + 1):
	file_name = 'RC_2009-0' + str(NUM)
	print(file_name)
	with open(file_name) as file:
		data = json.load(file)
		for i, datum in enumerate(data):
			if i % 1000 == 0:
				print(i, '/', len(data))
			# if i > 10000:
			# 	break
			words = preprocess_text(datum['body'])
			for word in words:
				freqs[word] = freqs.get(word, 0) + 1
				count += 1

ratios = {}
for word in financial_freqs:
	if financial_freqs[word] >= 10:
		financial_perc = financial_freqs[word] / float(financial_count)
		if word in freqs:
			perc = freqs[word] / float(count)
		else:
			perc = 1 / float(count)
		
		ratio = financial_perc / perc
		ratios[word] = ratio

print(ratios)
print(financial_count, count)

with open('ratios.json', 'w') as file:
	json.dump(ratios, file)



