#!/usr/bin/python

import praw
import datetime

reddit = praw.Reddit('AggieBot')                

plaeddit = reddit.subreddit('plaeddit')

now = datetime.datetime.now()

plaeddit.submit("This is a test", selftext="This is the body of the message", send_replies=False)
