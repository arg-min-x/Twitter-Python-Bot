# Imports
import time
import warnings
from twitterTools import *
import tweepy
import MySQLdb
from threading import Timer

# suppress all warnings
warnings.filterwarnings("ignore")

# Create twitter object
twitter = twitterTools()
twitter.authenticate('access_key.csv')

# Open database connection
db = MySQLdb.connect("localhost","root","","twitterTest" )

# Setup Timers
def timeout():
    return 0
followerResetCount = 5          # How many people to follower before timeout
followerTimerLength = 20        # How long to time out in seconds
followerTimer = Timer(5,timeout)# Timer object
followerCount = 0               # follower count index
maxFollowers = 450
unfollowCount = 10               # number of people to unfollow once max is reached
currentlyFollowingcount = twitter.api.me().friends_count # How many people I'm currently follwoing
time.sleep(5.1)
try:
    # Main loop looks through NASA's followers and follows people with high
    # friends to followers count
    for followers in tweepy.Cursor(twitter.api.followers,screen_name = 'taylorswift13').items():
    # for followers in tweepy.Cursor(twitter.api.friends).items():

        # check if user ID is already in the databse
        userInDatabase = twitter.isInDatabase(followers.id,db)
        if userInDatabase:
            print "user already in database " + followers.screen_name
            # Update user information

        else:
            # Prepare SQL query to INSERT a record into the database.
            twitter.userToMysql(followers,db)
            print "user not in database " + followers.screen_name
            
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
                if float(followers.followers_count)/float(followers.friends_count) >= 0.2:
                    followers.follow()
                    twitter.updateFollowing(followers.id,1,db)
                    print 'Now following ' + followers.screen_name
                    followerCount += 1
                    currentlyFollowingcount += 1
                    
        # Check if my friend count is too high
        if currentlyFollowingcount >= maxFollowers:

            # # Recrawl all people following me update the follower flag in db
            # for follower in tweepy.Cursor(twitter.api.followers).items():
            #     print "recrawling followers"
            #     if twitter.isInDatabase(follower.id,db):
            #         twitter.updateFollower(follower.id, 1, db)
            #     else:
            #         twitter.userToMysql(follower,db)
            #         twitter.updateFollower(follower.id, 1, db)
            #
            #     # sleep to avoid rate limits
            #     time.sleep(5.1)

            # Return a list of all people I'm following
            mysqlString = "select id,follower,dateCrawled,screenName from user2\
                            where following=1 order by dateCrawled ASC;"
            # Execute the SQL command
            cursor = db.cursor()
            cursor.execute(mysqlString)
            followingList = cursor.fetchall()

            # Loop through people and unfollow old people not following me
            unfollowInd = 0
            for col in followingList:
                # check if they are following me
                if not col[1]:
                    # Unfollow some people
                    print "unfollowing " + col[3]
                    twitter.api.destroy_friendship(id=col[0])
                    twitter.updateFollowing(col[0],0,db)
                    unfollowInd += 1
                    time.sleep(5.1)
                if unfollowInd >= unfollowCount:
                    break

            # Reset the follower count
            currentlyFollowingcount = twitter.api.me().friends_count
            time.sleep(5.1)

        # Sleep to avoid rate limits
        time.sleep(5.1)
        
    # disconnect from server
    db.close()

# Handle keyboard interrupte
except(KeyboardInterrupt):
    # disconnect from server
    db.close()
    print "Keyboard interupt detected"
    raise SystemExit

