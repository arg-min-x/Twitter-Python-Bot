import csv
import tweepy

# Strean listener class that overrides on_status function
class MyStreamListener(tweepy.StreamListener):
    
    def on_status(self, status):
        print(status.text)

# Streamer class
class twitterStreamer:
    
    # Initilize the class
    def __init__(self):
        self.APP_KEY = ''
        self.APP_SECRET = ''
        self.ACCESS_TOKEN = ''
        self.ACCESS_TOKEN_SECRET = ''
        self.api = 0
        self.stream_listener = 0
        self.stream = 0
        
    # Authenticate to the twitter account with credentials stored in the csv
    # file name "fileName"
    def _authenticate(self,fileName):
        
        # Get key information from csv fileName
        with open(fileName, 'rb') as csvfile:
            keyReader = csv.reader(csvfile, delimiter=',', quotechar='|')
            first_row = keyReader.next()
            APP_KEY = first_row[0]
            APP_SECRET = first_row[1]
            ACCESS_TOKEN = first_row[2]
            ACCESS_TOKEN_SECRET = first_row[3]
        
        # Authenticate
        auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    # Start the streamer for public tweets
    def _start_stream(self):

        self.stream_listener = MyStreamListener()
        self.stream = tweepy.Stream(auth = self.api.auth, listener=MyStreamListener())



