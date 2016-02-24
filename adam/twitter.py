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

# Setup Timers
def timeout():
    return 0
followerResetCount = 3          # How many people to follower before timeout
followerTimerLength = 20        # How long to time out in seconds
followerTimer = Timer(5,timeout)# Timer object
followerCount = 0;              # follower count index

try:
    # Main loop looks through NASA's followers and follows people with high
    # friends to followers count
    ##for followers in tweepy.Cursor(twitter.api.followers,screen_name = 'taylorswift13').items():
    for followers in tweepy.Cursor(twitter.api.followers).items():

        # check if user ID is already in the databse
        userInDatabase = twitter.isInDatabase(followers.id,db)
        if userInDatabase:
            print "user already in database"
            print followers.screen_name
            twitter.updateFollowing(followers.id,1,db)
        else:
            # Prepare SQL query to INSERT a record into the database.
            twitter.userToMysql(followers,db)
            print "user not in database"
            
        # Start a timer to limit followers per day
        if followerCount == followerResetCount:
            print ("Followed the maximum number of people for this "
                   "session timing out")
            followerTimer = Timer(followerTimerLength,timeout)
            followerTimer.start()
            followerCount = 0
            
        # Check if the timer is running for follower reset
        if not followerTimer.isAlive():
            # check to make sure they have followers
            if followers.friends_count > 0:
                if followers.followers_count/followers.friends_count >= 0:
                    followers.follow()
                    print 'Now following ' + followers.screen_name
                    followerCount += 1
                    print followerCount
                    
        # Check if my friend count is too high
        if twitter.api.me().friends_count >= 400:
            print "put unfollow code here"
            mysqlString = "select screenName,following,dateCrawled from user2\
                           where following=1 order by dateCrawled DESC;"
            
        #print '.'
        time.sleep(5.1)
        
    # disconnect from server
    db.close()

# Handle keyboard interrupt
except(KeyboardInterrupt):
    # disconnect from server
    db.close()
    print "Keyboard interupt detected"
    raise SystemExit
##except:
##    # disconnect from server
##    db.close()
##    raise






# Main loop looks through NASA's followers and follows people with high
# friends to followers count
##for followers in tweepy.Cursor(twitter.api.followers,id=11348282,cursor = -1).items():
##
##    # check to make sure they have followers
##    if followers.friends_count > 0:
##        if followers.followers_count/followers.friends_count > 0:
##            followers.follow()
##            follower_count += 1
##            print 'Now following ' + followers.screen_name
##    # Sleep for 8 seconds to avoid rate limits
##    print '.'        
##    time.sleep(3)
        




