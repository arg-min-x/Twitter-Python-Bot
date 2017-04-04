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
followerTimerLength = 10        # How long to time out in seconds
followerTimer = Timer(5,timeout)# Timer object
followerCount = 0               # follower count index
maxFollowers = 450
unfollowCount = 5               # number of people to unfollow once max is reached
currentlyFollowingcount = twitter.api.me().friends_count # How many people I'm currently follwoing
# time.sleep(5.1)
twitter.table = "taylorswift13Followers"
try:
    # Main loop looks through NASA's followers and follows people with high
    # friends to followers count
    dBcursor = db.cursor()
    dbString = "SELECT id,follower,dateCrawled,screenName,friendsCount,followersCount FROM %s WHERE following=0 AND followedInPast=0 ORDER by dateCrawled ASC LIMIT 100;" % (twitter.table)
    dBcursor.execute(dbString)

    for row in range(0,dBcursor.rowcount):
        row = dBcursor.fetchone()

        # convert a row into an object for easy interpetation
        id = row[0]
        follower = row[1]
        dateCrawled = row[1]
        screen_name = row[3]
        friends_count = row[4]
        followers_count = row[5]

        # Start a timer to limit followers per day
        if followerCount == followerResetCount:
            print ("Followed the maximum number of people for this session timing out %s") %(strftime("%Y-%m-%d %H:%M:%S", localtime()))
            followerTimer = Timer(followerTimerLength,timeout)
            followerTimer.start()
            twitter.waitForTimer(followerTimer)
            followerCount = 0

        # check to make sure they have followers
        if friends_count > 0:
            if float(followers_count)/float(friends_count) >= 0.2:

                # Follow this person
                tmpuser = twitter.api.get_user(id=id)
                tmpuser.follow()
                twitter.updateFollowing(id,1)
                print 'Now following %s %s' %(screen_name,strftime("%Y-%m-%d %H:%M:%S", localtime()))
                followerCount += 1
                currentlyFollowingcount += 1
                time.sleep(5.1)
                    
        # Check if my friend count is too high
        if currentlyFollowingcount >= maxFollowers:

            # Recrawl all people following me update the follower flag in db
            for followerPages in tweepy.Cursor(twitter.api.followers,count=200).pages():
                print "recrawling followers %s" %(strftime("%Y-%m-%d %H:%M:%S", localtime()))
                rateTimer = Timer(61,timeout)
                rateTimer.start()

                for follower in followerPages:
                    twitter.userToMysql(follower)
                    twitter.updateFollower(follower.id, 1)

                # Avoid Rate Limts
                twitter.waitForTimer(rateTimer)

            # Return a list of all people I'm following
            mysqlString = "select id,follower,dateCrawled,screenName from %s\
                            where following=1 order by dateCrawled ASC;" %(twitter.table)
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
                    print "unfollowing %s %s" %(col[3], strftime("%Y-%m-%d %H:%M:%S", localtime()))
                    twitter.api.destroy_friendship(id=col[0])
                    twitter.updateFollowing(col[0],0)
                    unfollowInd += 1
                    time.sleep(5.1)
                if unfollowInd >= unfollowCount:
                    break

            # Reset the follower count
            currentlyFollowingcount = twitter.api.me().friends_count
            time.sleep(5.1)
        
    # disconnect from server
    db.close()

# Handle keyboard interrupte
except(KeyboardInterrupt):
    # disconnect from server
    db.close()
    print "Keyboard interupt detected"
    raise SystemExit

