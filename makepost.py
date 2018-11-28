#!/usr/bin/python

import praw
import datetime
import time

reddit = praw.Reddit('AggieBot')
plaeddit = reddit.subreddit('plaeddit')

def make_daily_post():
    water_command = 'water'
    no_water_command = 'no water'
    light_command = 'light'
    no_light_command = 'no light'

    now = datetime.datetime.now()
    day = now.day if now.day > 9 else '0' + str(now.day)
    title = '[' + str(now.month) + '/' + str(day) + '/' + str(now.year) + '] ' + 'Daily instruction thread'
    body = '''It's that time of day again, so it's time to submit your vote on
    which action I should take to keep the plant alive! Replies containing
    only `''' + water_command +'''` will be a vote for watering the plant.
    Replies containing only `''' + no_water_command + '''` will be a vote for
    not watering the plant. Replies containing
    only `''' + light_command +'''` will be a vote for lighting the plant.
    Replies containing only `''' + no_light_command + '''` will be a vote for
    not lighting the plant.
    Any replies not containing one of these four phrases will be ignored!
    All voting for the day must be completed by 5:00pm Central Time. &nbsp;
    When your vote has been tallied, I will reply to your post!'''

    submission = plaeddit.submit(title, selftext=body, send_replies=False)


# ----------- MAIN -----------

make_daily_post()
