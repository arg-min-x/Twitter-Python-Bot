import warnings
from twitterStreamer import *

# Suppress all warnings
warnings.filterwarnings("ignore")

# Initialize the stream
twitter = twitterStreamer()

# Authenticate and start the stream
twitter._authenticate('access_key.csv')
twitter._start_stream()

# Define how to use the streamer
twitter.stream.filter(locations=[-83.163757,39.866534,-82.832794,40.128491])




        




