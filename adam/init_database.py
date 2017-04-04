# Imports
import time
import warnings
from twitterTools import *
from threading import Timer

# supress all warnings
warnings.filterwarnings("ignore")

# Setup Timers
def timeout():
    print "timer up"
waitTime = 61
waitTimer = Timer(waitTime,timeout)# Timer object

# Create twitter object
twitter = twitterTools()
twitter.authenticate('access_key.csv')
twitter.table = "taylorswift13Followers"
pageCount = 200

# Crawl people I am currently following and add them to the datbase
try:
    for friendsPages in tweepy.Cursor(twitter.api.friends,count=pageCount).pages():
        waitTimer = Timer(waitTime,timeout) # Timer object
        waitTimer.start()
        for friends in friendsPages:
            twitter.userToMysql(friends)
            twitter.updateFollowing(friends.id,1)
            print friends.screen_name
        twitter.waitForTimer(waitTimer)

except(KeyboardInterrupt):
    # disconnect from server
    twitter.closeDb()
    print "Keyboard interupt detected"

# Crawl people currently following me and update follower status
try:
    for followerPages in tweepy.Cursor(twitter.api.followers,count=pageCount).pages():
        waitTimer = Timer(waitTime,timeout)# Timer object
        waitTimer.start()
        for follower in followerPages:
            print follower.screen_name
            twitter.userToMysql(follower)
            twitter.updateFollower(follower.id, 1)
        twitter.waitForTimer(waitTimer)

    # disconnect from server
    twitter.closeDb()
    
except(KeyboardInterrupt):
    # disconnect from server
    twitter.closeDb()
    print "Keyboard interupt detected"
