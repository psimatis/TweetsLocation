import tweepy
import json

# pick your bounding box
USA = [-132.714844, 22.917923, -50.097656, 50.847573]
# earth = [-180, -90, 180, 90]

conKey = '...'
conSKey = '...'
accessToken = '...'
accessSToken = '...'

count = 0
writeFile = open('tweets.txt', 'a')

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        if tweet.coordinates is not None:
            temp = str(tweet.coordinates).split('[')[1]
            x = float(temp.split(',')[0])
            y = float(temp.split(',')[1][:-3])
            print(x, y, tweet.text)
            global count 
            count += 1
            writeFile.write(str(count) + ' ' + str(x) + ' ' + str(y) + '\n')
        
    def on_error(self, status):
        print("Error detected")

auth = tweepy.OAuthHandler(conKey, conSKey)
auth.set_access_token(accessToken, accessSToken)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(locations=USA)
