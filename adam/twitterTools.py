import csv
import tweepy
from time import localtime, strftime

class twitterTools:
    def __init__(self):
        self.APP_KEY = ''
        self.APP_SECRET = ''
        self.ACCESS_TOKEN = ''
        self.ACCESS_TOKEN_SECRET = ''
        self.api = 0
        self.database = []
        
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
    def userToMysql(self,user,database):
        # Prepare SQL string to INSERT a record into the database.
        user.description = user.description.replace("\'", "\\\'")
        user.location = user.location.replace("\'", "\\\'")
        user.name = user.name.replace("\'", "\\\'")
        user.following = int(user.following)
        user.default_profile = int(user.default_profile)
        user.verified = int(user.verified)
        user.follow_request_sent = int(user.follow_request_sent)
        user.created_at = user.created_at.isoformat()
        user.created_at = user.created_at.replace('T',' ')
        if user.time_zone:
            user.time_zone = user.time_zone.replace("\'", "\\\'")

        dateCrawled = strftime("%Y-%m-%d %H:%M:%S", localtime())
        
        mysqlString = ("INSERT INTO user2(screenName,name,ID, description, location,"
                       "following, friendsCount, followersCount, favouritesCount, "
                       "defaultProfile, verified, followRequestSent, timezone, "
                       "dateCreated, dateCrawled) VALUES ('%s', '%s', %d, '%s', "
                       "'%s', %d, %d, %d, %d, %d, %d, %d, '%s', '%s', '%s');")\
                       % (user.screen_name, user.name, user.id, user.description, \
                          user.location, user.following, user.friends_count,\
                          user.followers_count,user.favourites_count, user.default_profile,\
                          user.verified, user.follow_request_sent, user.time_zone,\
                          user.created_at, dateCrawled)
        mysqlString = mysqlString.encode('ascii',errors='ignore')

        # prepare a cursor object using cursor() method
        cursor = database.cursor()
        try:
           # Execute the SQL command
           cursor.execute(mysqlString)
           # Commit your changes in the database
           database.commit()
        except:
           # Rollback in case there is any error
           database.rollback()
           print mysqlString

    # Check if a user is already in the database
    def isInDatabase(self,ID,database):
        
        # prepare a cursor object using cursor() method
        cursor = database.cursor()

        # Prepare SQL query to INSERT a record into the database.
        mysqlString = "SELECT * FROM user2 \
               WHERE ID LIKE %d" %(ID)
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
            print "Error: unable to fecth data"
            inDatabase = 1
        
        return inDatabase

