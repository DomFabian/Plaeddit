#!/usr/bin/python

import praw
import datetime
import time
import RPi.GPIO as io

reddit = praw.Reddit('AggieBot')                
plaeddit = reddit.subreddit('plaeddit')

# set up the pins
io.setmode(io.BOARD)
io.setwarnings(False)
pump_pin = 38
io.setup(pump_pin, io.OUT)

def make_daily_post():
    water_command = 'water'
    no_water_command = 'no water'
    light_command = ''
    no_light_command = ''

    now = datetime.datetime.now()
    day = now.day if now.day > 9 else '0' + str(now.day)
    title = '[' + str(now.month) + '/' + str(day) + '/' + str(now.year) + '] ' + 'Daily instruction thread'
    body = '''It's that time of day again, so it's time to submit your vote on which action I should take to keep the plant alive! Replies containing only `''' + water_command +'''` will be a vote for watering the plant. Replies containing only `''' + no_water_command + '''` will be a vote for not watering the plant. Any replies not containing one of these two phrases will be ignored! All voting for the day must be completed by 5:00pm Central Time.

&nbsp;

When your vote has been tallied, I will reply to your post!'''

    submission = plaeddit.submit(title, selftext=body, send_replies=False)

def get_todays_post():
    ''' returns the Submission object for today's post '''
    now = datetime.datetime.now()
    day = now.day if now.day > 9 else '0' + str(now.day)
    query = '[' + str(now.month) + '/' + str(day) + '/' + str(now.year) + ']'
    submissions = plaeddit.new()

    for submission in submissions:
        if submission.title[:12] == query:
            print "Today's post located"
            return submission

    # if we get here then we can't find today's post!!
    return None

def tally_votes(submission):
    ''' takes in a submission object and tallies the votes in it.
    this function returns an integer water_votes (pos means water, neg means no water)
    and an integer total_votes '''
    water_votes = 0
    total_votes = 0
    for comment in submission.comments:
        already_seen = False

        # ignore posts that I make
        if comment.author == "AggieBot":
            continue

        # check to see if I have seen this comment already
        for reply in comment.replies:
            if reply.author == 'AggieBot':
                # we've already tallied this post
                already_seen = True
                break

        if not already_seen:
            # search for the keywords
            vote = parse_comment(comment.body)

            # reply to the comment
            vote_text = ""
            if vote == 1:
                vote_text = "water"
            elif vote == -1:
                vote_text = "not water"
            elif vote == 0:
                # remove the comment
                comment.delete()
                continue
            body = "Understood! I'll tally your vote to " + vote_text + " the plant!"
            comment.reply(body)

            # count the vote
            water_votes += vote
            total_votes += 1

    return water_votes, total_votes


def parse_comment(text):
    ''' this function takes in a string representing the body of a comment and 
    returns either a 1 symbolizing `water` or a -1 symbolizing `not water`
    default case to return 0 for invalid comment '''

    previous_word = ""
    for word in text.split():
        if word == "water":
            return -1 if previous_word == "no" else 1
        previous_word = word

    # handle case where there is no clear vote
    return 0

def pump_water(time_sec):
    if time_sec > 10:
        print('No')
        return
    io.output(pump_pin, io.HIGH)
    time.sleep(time_sec)
    io.output(pump_pin, io.LOW)


# ----------- MAIN -----------

post = get_todays_post()
if post is not None:
    water_votes, total_votes = tally_votes(get_todays_post())
    print "water_votes = " + str(water_votes)
    print "total_votes = " + str(total_votes)

    if water_votes > 0:
        pump_water(5)

