# Imports
import time
import warnings
from twitterTools import *
import MySQLdb
import tweepy
from threading import Timer

# supress all warnings
warnings.filterwarnings("ignore")

# Create twitter object
twitter = twitterTools()
twitter.authenticate('access_key.csv')

# Open database connection
db = MySQLdb.connect("localhost","root","","twitterTest" )

screenName = 'taylorswift13'
pageCount = 200
try:
    for followerPages in tweepy.Cursor(twitter.api.followers,screen_name=screenName,count=pageCount).pages():
        for followers in followerPages:
            # check if user ID is already in the databse
            userInDatabase = twitter.isInDatabase(followers.id,db)
            if userInDatabase:
                # print "user already in database " + followers.screen_name
                # Update user information
                x = 0
            else:
                # Prepare SQL query to INSERT a record into the database.
                twitter.userToMysql(followers,db)
                # print "user not in database " + followers.screen_name

        # Avoid Rate Limts
        time.sleep(61)

    db.close()
except(KeyboardInterrupt):
    # disconnect from server
    db.close()
    print "Keyboard interupt detected"
    raise SystemExit

