#Import the necessary methods from tweepy library
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from translate import Translator  #https://github.com/terryyin/translate-python
translator = Translator(to_lang='fa')

#Variables that contains the user credentials to access Twitter API
consumer_key = "you should generate it for yourself at dev.twitter"
consumer_secret = "you should generate it for yourself at dev.twitter"
access_token = "you should generate it for yourself at dev.twitter"
access_token_secret = "you should generate it for yourself at dev.twitter"

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        saveFile = open('./filteresStream.txt', 'a')
        saveFile.write(data)
        saveFile.write('\n')
        saveFile.close()
        tweet_text = data.split(',"text":"')[1].split('","source')[0]
        print tweet_text
        translation = translator.translate(tweet_text)
        print 'translation:', translation
        return True

    def on_error(self, status):
        if status == 420:
            print 'error',status
            # returning False in on_error disconnects the stream
            return False
        # returning non-False reconnects the stream, with backoff.
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    #stream.filter(track=['python', 'javascript', 'ruby'])


    #creating a list of (id/user_id/screen_name) of the persons you want to follow on stream
    mylist = ['SaeedTaghaviV', 'NewYorker', 'Cyberattac_Newz']
    mylistID = []
    for person in mylist:
        user = api.get_user(person)
        mylistID = mylistID + [str(user.id)]
    print mylistID

    #folList=['941235626136842240', '14706299', '895988202498076672', '798112091202875392']
    folList = mylistID
    # how to use filter to stream tweets by a specific user. The follow parameter is an array of IDs
    stream.filter(follow=folList)

    #stream.filter(follow = mylistID )
