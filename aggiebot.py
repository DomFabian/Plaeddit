#!/usr/bin/python

import praw
import time
import datetime

reddit = praw.Reddit(user_agent='<removed>',
                     client_id='<removed>',
                     client_secret='<removed>',
                     username='AggieBot',
                     password='')
reddit.read_only = False                 

plaeddit = reddit.subreddit('plaeddit')

def main():
    now = datetime.datetime.now()

    plaeddit.submit("This is a test", selftext="This is the body of the message", url="www.tamu.edu", send_replies=False)

main()
