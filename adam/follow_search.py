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
for friend in tweepy.Cursor(twitter.api.friends).items():
    # Process the friend here
    print friend.created_at

    # Prepare SQL query to INSERT a record into the database.
    sql = twitter.userToMysql(friend)

    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Commit your changes in the database
       db.commit()
    except:
       # Rollback in case there is any error
       db.rollback()    # Execute the SQL command
       print 'f up'
       print sql

    print '.'
    time.sleep(6)
        
## disconnect from server
db.close()
    
    
    

    
