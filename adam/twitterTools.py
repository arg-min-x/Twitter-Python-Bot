import csv
import tweepy
from time import localtime, strftime
import MySQLdb
import time

class twitterTools:
    def __init__(self):
        self.APP_KEY = ''
        self.APP_SECRET = ''
        self.ACCESS_TOKEN = ''
        self.ACCESS_TOKEN_SECRET = ''
        self.api = 0

        # Open database connection
        self.db = MySQLdb.connect("localhost","root","","twitter" )
        self.table = "twitter"

    # authenticate to the twitter account with credentials stored in the csv
    # file name "fileName"
    def authenticate(self,fileName):
        # Get key information from csv fileName
        with open(fileName, 'rb') as csvfile:
            keyReader = csv.reader(csvfile, delimiter=',', quotechar='|')
            first_row = keyReader.next()
            APP_KEY = first_row[0]
            APP_SECRET = first_row[1]
            ACCESS_TOKEN = first_row[2]
            ACCESS_TOKEN_SECRET = first_row[3]
        # authenticate
        auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    # Convert user information into a string and insert into MySQL database
    def userToMysql(self,user):
        # Prepare SQL string to INSERT a record into the database.
        user.description = user.description.replace("\'", "\\\'")
        user.location = user.location.replace("\'", "\\\'")
        user.name = user.name.replace("\'", "\\\'")
        user.following = int(user.following)
        user.default_profile = int(user.default_profile)
        user.geo_enabled = int(user.geo_enabled)
        user.verified = int(user.verified)
        user.follow_request_sent = int(user.follow_request_sent)
        user.created_at = user.created_at.isoformat()
        user.created_at = user.created_at.replace('T',' ')
        if user.time_zone:
            user.time_zone = user.time_zone.replace("\'", "\\\'")

        dateCrawled = strftime("%Y-%m-%d %H:%M:%S", localtime())
        
        mysqlString = ("INSERT IGNORE INTO %s(screenName,name,ID, description, location,"
                       "following, friendsCount, followersCount, favouritesCount, statusesCount, "
                       "defaultProfile, verified, geoEnabled, followRequestSent, timezone, "
                       "dateCreated, dateCrawled) VALUES ('%s', '%s', %d, '%s', "
                       "'%s', %d, %d, %d, %d, %d, %d, %d, %d, %d, '%s', '%s', '%s');")\
                       % (self.table,user.screen_name, user.name, user.id, user.description, \
                          user.location, user.following, user.friends_count,\
                          user.followers_count,user.favourites_count, user.statuses_count, user.default_profile,\
                          user.verified, user.geo_enabled, user.follow_request_sent, user.time_zone,\
                          user.created_at, dateCrawled)
        mysqlString = mysqlString.encode('ascii',errors='ignore')

        # prepare a cursor object using cursor() method
        cursor = self.db.cursor()
        try:
           # Execute the SQL command
           cursor.execute(mysqlString)
           # Commit your changes in the database
           self.db.commit()
        except:
           # Rollback in case there is any error
           self.db.rollback()
           print mysqlString

    # Check if a user is already in the database
    def isInDatabase(self,ID):
        
        # prepare a cursor object using cursor() method
        cursor = self.db.cursor()

        # Prepare SQL query to INSERT a record into the database.
        mysqlString = "SELECT * FROM %s \
               WHERE ID LIKE %d" %(self.table,ID)
        try:
            # Execute the SQL command
            cursor.execute(mysqlString)
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
    
            if results:
                inDatabase = 1
            else:
                inDatabase = 0
                
        except:
            print "Error: unable to fetch data"
            inDatabase = 1
        
        return inDatabase

    # Update friend status in the database
    def updateFollower(self, ID, isFollower):

        # prepare a cursor object using cursor() method
        cursor = self.db.cursor()
        
        mysqlString = "UPDATE %s SET follower = %d WHERE id = %d;" %(self.table,isFollower, ID)
        mysqlString = mysqlString.encode('ascii',errors='ignore')

        try:
            # Execute the SQL command
            cursor.execute(mysqlString)
            self.db.commit()
        except:
            print "Error: unable to fetch data"
            # Rollback in case there is any error
            self.db.rollback()
            print mysqlString

    # Update friend status in the database
    def updateFollowing(self, ID, isFollowing):

        # prepare a cursor object using cursor() method
        cursor = self.db.cursor()
        
        mysqlString = "UPDATE %s SET following = %d,followedInPast=1,dateFollowed='%s' WHERE id = %d;" %(self.table,isFollowing, strftime("%Y-%m-%d %H:%M:%S", localtime()), ID)
        mysqlString = mysqlString.encode('ascii',errors='ignore')

        try:
            # Execute the SQL command
            cursor.execute(mysqlString)
            self.db.commit()
        except:
            print "Error: unable to fecth data"
            # Rollback in case there is any error
            self.db.rollback()
            print mysqlString


    # Close the database
    def closeDb(self):
        self.db.close()

    # Wait for the timer to finish
    def waitForTimer(self,timer):
        wait = 1
        while wait:
            if not timer.isAlive():
                wait = 0
            time.sleep(1)

