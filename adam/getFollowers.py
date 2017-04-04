# nohup nice python -u getFollowers.py > trumplog1.txt &

# nohup nice python getFollowers.py

# Imports
import time
import warnings
from twitterTools import *
import MySQLdb
import tweepy
from threading import Timer
from sys import argv
import os
import logging

# suppress all warnings
warnings.filterwarnings("ignore")

# Start the log file
LOG_FILENAME = 'trump.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.ERROR)

# Save PID to monitor process
pid = str(os.getpid())
currentFile = open("/home/adam/monit_test.pid", "w")
currentFile.write(pid)
currentFile.close()

# Setup Timers
def timeout():
    return 0
waitTime = 61
waitTimer = Timer(waitTime,timeout)# Timer object

# Create twitter object
twitter = twitterTools()
twitter.authenticate('access_key.csv')

# Set some parameters
screenName = "realDonaldTrump"
twitter.table = "donaldTrumpFollowers"
pageCount = 200

# Get the last cursor position
currentFile = open("/home/adam/last_cursor_trump.txt", "r")
next_cursor = int(currentFile.read())
currentFile.close()
print next_cursor

pagination = tweepy.Cursor(twitter.api.followers,screen_name=screenName,count=pageCount,cursor=next_cursor).pages()
try:
    for followerPages in pagination:

       # Start a timer
       waitTimer = Timer(waitTime,timeout) # Timer object
       waitTimer.start()

       # print pagination.current_page
       next_cursor = pagination.next_cursor
       logging.error(str(next_cursor))

       # Save the next cursor for future use
       currentFile = open("/home/adam/last_cursor_trump.txt", "w")
       currentFile.write(str(next_cursor))
       currentFile.close()

       # add all followers on the page to the database
       for followers in followerPages:
           twitter.userToMysql(followers)
           #print followers.screen_name

       # Avoid Rate Limts
       twitter.waitForTimer(waitTimer)

    # Close the database
    twitter.closeDb()

except(KeyboardInterrupt):
   # disconnect from server
    twitter.closeDb()
  # print "Keyboard interupt detected"
   #raise SystemExit
except:
   print next_cursor
    # disconnect from server
   twitter.closeDb()

