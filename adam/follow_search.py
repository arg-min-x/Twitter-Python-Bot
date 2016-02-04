import time
import warnings
from twitterTools import *
import MySQLdb

# supress all warnings
warnings.filterwarnings("ignore")

twitter = twitterTools()
twitter.authenticate('access_key.csv')

# Open database connection
db = MySQLdb.connect("localhost","root","","twitterTest" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

#for friend in tweepy.Cursor(twitter.api.friends,screen_name = 'CLCShareCloud').items(1):
##for friend in tweepy.Cursor(twitter.api.followers, screen_name = 'taylorswift13').items():
for friend in tweepy.Cursor(twitter.api.followers).items():

    # check if user ID is already in the databse
    userInDatabase = twitter.isInDatabase(friend.id,db)
    if userInDatabase:
        print "user already in database"
    else:
        # Prepare SQL query to INSERT a record into the database.
        twitter.userToMysql(friend,db)

    #print '.'
    time.sleep(5.1)
        
## disconnect from server
db.close()
    
    
    

    
