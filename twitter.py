import time
import warnings
from twitterTools import *

# supress all warnings
warnings.filterwarnings("ignore")

twitter = twitterTools()
twitter.authenticate('access_key.csv')

# Main loop looks through NASA's followers and follows people with high
# friends to followers count
follower_count = 0;
for followers in tweepy.Cursor(twitter.api.followers,id=11348282,cursor = -1).items():

    # check to make sure they have followers
    if followers.friends_count > 0:
        if followers.followers_count/followers.friends_count > 0.2:
            followers.follow()
            follower_count += 1
            print 'Now following ' + followers.screen_name
    # Sleep for 8 seconds to avoid rate limits
    print '.'        
    time.sleep(8)
        




