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

    # Convert user information into a string for addition to MySQL database
    def userToMysql(self,user):
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

        dateCrawled = strftime("%Y-%m-%d %H:%M:%S", localtime())
        
        mysqlString = "INSERT INTO user(screenName,name,ID, description, location, following, friendsCount, followersCount, favouritesCount, defaultProfile, verified, followRequestSent, dateCreated, dateCrawled) VALUES ('%s', '%s', %d, '%s', '%s', %d, %d, %d, %d, %d, %d, %d, '%s', '%s');"\
          % (user.screen_name, user.name, user.id, user.description, user.location, user.following, user.friends_count,user.followers_count,user.favourites_count, user.default_profile, user.verified, user.follow_request_sent, user.created_at, dateCrawled)
        mysqlString = mysqlString.encode('ascii',errors='ignore')
        return mysqlString
