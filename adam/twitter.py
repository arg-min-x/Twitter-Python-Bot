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
followerCount = 0               # follower count index
maxFollowers = 1000
currentlyFollowingcount = twitter.api.me().friends_count # How many people I'm currently follwoing
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
                if float(followers.followers_count)/float(followers.friends_count) >= 0.1:
                    followers.follow()
                    twitter.updateFollowing(followers.id,1,db)
                    print 'Now following ' + followers.screen_name
                    followerCount += 1
                    currentlyFollowingcount += 1
                    print currentlyFollowingcount
                    
        # Check if my friend count is too high
        if currentlyFollowingcount >= maxFollowers:

            # Recrawl all people following me update the follower flag in db
            for follower in tweepy.Cursor(twitter.api.followers).items():
                if twitter.isInDatabase(follower.id,db):
                    twitter.updateFollower(follower.id, 1, db)
                else:
                    twitter.userToMysql(follower,db)
                    twitter.updateFollower(follower.id, 1, db)
                    
                # sleep to avoid rate limits
                time.sleep(5.1)

            # Return a list of all people I'm following
            mysqlString = "select screenName,following,follower,dateCrawled from user2\
                            where following=1 order by dateCrawled ASC;"
            # Execute the SQL command
            cursor = db.cursor()
            cursor.execute(mysqlString)
            followingList = cursor.fetchall()

            # Loop through people and unfollow old people not following me
            for col in followingList:
                # check if they are following me
                if not col[1]:
                    # Put unfollow code here for people who aren't following me
                    # NEED TO FIGURE OUT HOW MANY PEOPLE TO UNFOLLOW
                    print col[0]
                    print col[1]
            time.sleep(5.1)

            currentlyFollowingcount = twitter.api.me().friends_count 

        # Sleep to avoid rate limits
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

