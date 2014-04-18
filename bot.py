#nessesary libraries
from twitter import *
from time import *
import os.path
import datetime

#information nessesary to authenticate with twitter
OAUTH_TOKEN="YOUR_OAUTH_TOKEN"
OAUTH_SECRET="YOUR_OAUTH_SECRET"
CONSUMER_KEY="YOUR_CONSUMER_KEY"
CONSUMER_SECRET="YOUR_CONSUMER_SECRET"

search_query="YOUR_SEARCH_QUERY" #string to search for
save_file="lastid.txt" #file to save the id of the last tweet responded to.  
#This makes it so when the bot restarts it will not reply to the same tweet twice

wait_time=120 #keep this above 60 to prevent twitter from kicking you off the api


t = Twitter(
	auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
                       CONSUMER_KEY, CONSUMER_SECRET)
           )



#get last id read from the bot so that it does not reply to the same tweet
if(os.path.isfile(save_file)):
	f = open(save_file, 'r')
	last_id=int(f.read().strip())
	f.close()
else:
	last_id=0


while(True):
	searched=t.search.tweets(q=search_query,since_id=last_id) #get the tweets that match the query
	if len(searched['statuses'])>0:
		print "The following tweets matched the query "+search_query+" \n" 
		for tweets in searched['statuses']: #loop through them
			print tweets['user']['screen_name'];
			print tweets['text'] + "\n"
			#reply to the tweet
			t.statuses.update(status="@"+tweets['user']['screen_name']+" YOUR REPLY",in_reply_to_status_id=tweets['id'])
			if tweets['id']>last_id:
				last_id=tweets['id']; #update the last id read and the contents of the file
				f=open(save_file,'w')
				f.write(str(last_id))
				f.close()
			print "query completed at approx "+str(datetime.datetime.now().time())
			#show the time so that you know when the next query will occur
			sleep(wait_time)
	else:
		print "No tweets found since last check \n"
		print "query completed at approx "+str(datetime.datetime.now().time())
		sleep(wait_time)