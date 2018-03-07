import praw
import json
import datetime
import time
reddit = praw.Reddit(client_id='tJPMCPv9rwNJrA',
					 client_secret='5rcOdSXgSSBfV6iAOaz3PhPN4Lo',
					 user_agent='proseccodaddy')

subreddit = reddit.subreddit('personalfinance')

file_name = 'personalfinance.json'
open(file_name, 'w').close()

file = open(file_name,'w')
file.write('[')

count = 0
list_dicts = []

for year in range(2017, 2018):
	for month in range(1,12):

		startDate = datetime.date(year, month, 1)
		endDate = datetime.date(year, (month + 1) % 12, 1)

		startUnix = time.mktime(startDate.timetuple())
		endUnix = time.mktime(endDate.timetuple())

		for submission in subreddit.submissions(startUnix, endUnix):

			comment_bodies = ''
			comments = list(submission.comments)
			for comment in comments:
				try:
					comment_bodies += comment.body.encode('utf-8') + ' '
				except:
					pass

			sub_dict = {'title': submission.title.encode('utf-8'),
						'flair': submission.title.encode('utf-8'),
						'upvotes': submission.score,
						'body': submission.selftext.encode('utf-8'),
						'date': startUnix,
						'comments': comment_bodies}
			list_dicts.append(sub_dict)

			count += 1
			print count


			file.write(json.dumps(sub_dict))
			file.write(', ')

file.write(']')
file.close()