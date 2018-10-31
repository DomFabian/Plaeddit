#!/usr/bin/python

import praw
import datetime

reddit = praw.Reddit('AggieBot')                
plaeddit = reddit.subreddit('plaeddit')

def make_daily_post():
    water_command = 'water'
    no_water_command = 'no water'
    light_command = ''
    no_light_command = ''

    now = datetime.datetime.now()
    title = '[' + str(now.month) + '/' + str(now.day) + '/' + str(now.year) + '] ' + 'Daily instruction thread'
    body = '''It's that time of day again, so it's time to submit your vote on which action I should take to keep the plant alive! Replies containing only `''' + water_command +'''` will be a vote for watering the plant. Replies containing only `''' + no_water_command + '''` will be a vote for not watering the plant. Any replies not containing one of these two phrases will be ignored! All voting for the day must be completed by 5:00pm Central Time.

&nbsp;

When your vote has been tallied, I will reply to your post!'''

    submission = plaeddit.submit(title, selftext=body, send_replies=False)

def get_todays_post():
    ''' returns the Submission object for today's post '''
    now = datetime.datetime.now()
    query = '[' + str(now.month) + '/' + str(now.day) + '/' + str(now.year) + ']'
    submissions = plaeddit.search(query, sort='new', time_filter='week')
    return submissions.next()

def tally_votes(submission):
    ''' takes in a submission object and tallies the votes in it '''
    water_votes = 0
    no_water_votes = 0
    for comment in submission.comments:
        # search for the keywords

#make_daily_post()
#get_todays_post()
