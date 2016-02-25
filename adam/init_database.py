# Imports
import time
import warnings
from twitterTools import *
import MySQLdb
from threading import Timer

# supress all warnings
warnings.filterwarnings("ignore")

# Create twitter object
twitter = twitterTools()
twitter.authenticate('access_key.csv')

# Open database connection
db = MySQLdb.connect("localhost","root","","twitterTest" )

# Crawl people I am currently following and add them to the datbase
try:
    for friends in tweepy.Cursor(twitter.api.friends).items():
        twitter.userToMysql(friends,db)
        print friends.screen_name
        time.sleep(5.1)

    # disconnect from server
    db.close()
    
except(KeyboardInterrupt):
    # disconnect from server
    db.close()
    print "Keyboard interupt detected"

# Crawl people crurrently following me and update follwer status
try:
    for follower in tweepy.Cursor(twitter.api.followers).items():
        print follower.screen_name
        if twitter.isInDatabase(follower.id,db):
            twitter.updateFollower(follower.id, 1, db)

        else:
            twitter.userToMysql(follower,db)
            twitter.updateFollower(follower.id, 1, db)
        time.sleep(5.1)

    # disconnect from server
    db.close()
    
except(KeyboardInterrupt):
    # disconnect from server
    db.close()
    print "Keyboard interupt detected"
