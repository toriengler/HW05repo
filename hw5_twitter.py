from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk

## SI 206 - HW
## COMMENT WITH:
## Your section day/time: 4, Tues 2-3:30
## Any names of people you worked with on this assignment:Monica Siegel, Michelle Phillips

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts

url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching
CACHE_FNAME = 'twitter_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}
data=open(CACHE_FNAME, 'w')


#Finish parts 1 and 2 and then come back to this

#Code for Part 1:Get Tweets




def see_tweets(username, num_tweets):
    resource_url='https://api.twitter.com/1.1/search/tweets.json?q={}&count={}'.format(username, num_tweets)
    if resource_url in CACHE_DICTION:
        print('checking cache...')
        data=CACHE_DICTION[resource_url]
    else:
        print('fetching data..')
        r = requests.get(resource_url, auth = auth)
        data=json.loads(r.text)
        filew=open('tweet.json', 'w')
        filew.write(json.dumps(data, indent=4))
        filew.close()
        filew=open(CACHE_FNAME, 'w')
        CACHE_DICTION[resource_url]=data
        filew.write(json.dumps(CACHE_DICTION))
        filew.close()
    tweets=''
    for item in data['statuses']:
        tweets+=item['text']
    tokens=nltk.word_tokenize(tweets)
    freqDist = nltk.FreqDist(token for token in tokens if token.isalpha() and 'https' not in token and 'http' not in token and 'RT' not in token)
#Code for Part 2:Analyze Tweets
    for word, frequency in freqDist.most_common(5):
        print(word + " " + str(frequency))
    return CACHE_DICTION[resource_url]
see_tweets(username, num_tweets)
#Creates frequency distribution from list
#Notice how you can incorporate conditional statements here

#Loop through and print the words and frequencies for the most common 5 words






if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
