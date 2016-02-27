from datetime import datetime
import csv
import re
import tweepy
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

# Stream listener class that overrides on_status function
class MyStreamListener(tweepy.StreamListener):
    
    # Override the initialization
    def __init__(self, **kwargs):
    
        # Call the super constructor and then set the orientation
        super(MyStreamListener, self).__init__(**kwargs)
        
        # Initialize the keys and api
        self.APP_KEY = ''
        self.APP_SECRET = ''
        self.ACCESS_TOKEN = ''
        self.ACCESS_TOKEN_SECRET = ''
        self.api = 0
    
        # Add the vector for storing the tweets per hour
        self.tweets_per_hour = [0 for x in range(24)]
    
        # Set the current hour
        self.current_hour = re.search('[0-9]*:',str(datetime.now()))
        self.current_hour = re.search('[0-9]*',self.current_hour.group(0))
        self.current_hour = int(self.current_hour.group(0))
        
        # Set the current day
        self.current_day = re.search('[0-9]* ',str(datetime.now()))
        self.current_day = re.search('[0-9]*',self.current_day.group(0))
        self.current_day = int(self.current_day.group(0))
    
        # Authenticate the app
        self._authenticate('access_key.csv')
    
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
        authenticated = 0
        while not authenticated:
            try:
                auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
                auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
                self.api = tweepy.API(auth)
                authenticated = 1
            except KeyboardInterrupt:
                raise
            except:
                pass

    # Override the error function
    def on_error(self, status_code):

        # Print error
        print str(datetime.now())+" - Error: "+str(status_code)

        # Try to reconnect
        self._authenticate('access_key.csv')
    
    # Override the on_status method
    def on_status(self, status):
        
        # Find the hour
        tweet_hour = re.search('[0-9]*:',str(datetime.now()))
        tweet_hour = re.search('[0-9]*',tweet_hour.group(0))
        tweet_hour = int(tweet_hour.group(0))
        
        # Find the day
        tweet_day = re.search('[0-9]* ',str(datetime.now()))
        tweet_day = re.search('[0-9]*',tweet_day.group(0))
        tweet_day = int(tweet_day.group(0))
        
        # Check the hour
        if (tweet_hour != self.current_hour):
            
            # Send out the tweet
            tweet_sent = 0
            while not tweet_sent:
                try:
                    self.api.update_status('The Columbus, OH area has sent {} tweets in the last hour.'.format(self.tweets_per_hour[self.current_hour]))
                    tweet_sent = 1
                except KeyboardInterrupt:
                    raise
                except:
                    self._authenticate('access_key.csv')
            
            # Update the hour
            self.current_hour = tweet_hour
            
            # Check the day and update if needed
            if (tweet_day != self.current_day):

                # Plot the results and save
                plt.clf()
                y_pos = np.arange(len(self.tweets_per_hour))
                plt.barh(y_pos, self.tweets_per_hour, align='center', alpha=0.4)
                plt.yticks(y_pos, range(0,len(self.tweets_per_hour)))
                plt.ylim([-1,25])
                plt.xlabel('Number of Tweets')
                plt.ylabel('Hour')
                plt.title('Tweets per Hour')
                plt.savefig('Tweets_per_Day.png')

                # Send out the tweet
                tweet_sent = 0
                while not tweet_sent:
                    try:
                        self.api.update_with_media('Tweets_per_Day.png', 'The Columbus, OH area stats for yesterday.')
                        tweet_sent = 1
                    except KeyboardInterrupt:
                        raise
                    except:
                        self._authenticate('access_key.csv')

                # Update the day
                self.current_day = tweet_day
                
                # Reset the vector for storing the tweets per hour
                self.tweets_per_hour = [0 for x in range(24)]
            
            # Increment the tweet count
            self.tweets_per_hour[self.current_hour] = self.tweets_per_hour[self.current_hour] + 1
    
        else:
            
            # Increment the tweet count
            self.tweets_per_hour[self.current_hour] = self.tweets_per_hour[self.current_hour] + 1

# Streamer class
class twitterStreamer:
    
    # Initilize the class
    def __init__(self):
        
        self.APP_KEY = ''
        self.APP_SECRET = ''
        self.ACCESS_TOKEN = ''
        self.ACCESS_TOKEN_SECRET = ''
        self.api = 0
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

        self.stream = tweepy.Stream(auth = self.api.auth, listener=MyStreamListener())



