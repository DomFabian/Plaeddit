#!/usr/bin/python
from subprocess import call
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
    this function returns an integer water_votes (pos means water, neg means no water),
    an integer light_votes (pos means light, neg means no light),
    and an integer total_votes '''
    water_votes = 0
    light_votes = 0
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
            water_vote = parse_comment_water(comment.body)
            light_vote = parse_comment_light(comment.body)

            # reply to the comment
            water_vote_text = ""
            if water_vote == 1:
                water_vote_text = "water"
            elif water_vote == -1:
                water_vote_text = "not water"

            body = "Understood! I'll tally your vote to " + water_vote_text + " the plant!"
            comment.reply(body)

            light_vote_text = ""
            if light_vote == 1:
                light_vote_text = "light"
            elif light_vote == -1:
                light_vote_text = "not light"
            elif light_vote == 0:
                # remove the comment
                comment.delete()
                continue

            body = "Understood! I'll tally your vote to " + light_vote_text + " the plant!"
            comment.reply(body)

            # count the vote
            water_votes += water_vote
            light_votes += light_vote
            total_votes += 1

    return light_votes, water_votes, total_votes


def parse_comment_water(text):
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

def parse_comment_light(text):
    ''' this function takes in a string representing the body of a comment and
    returns either a 1 symbolizing `light` or a -1 symbolizing `no light`
    default case to return 0 for invalid comment '''

    previous_word = ""
    for word in text.split():
        if word == "light":
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
    light_votes, water_votes, total_votes = tally_votes(get_todays_post())
    print "light_votes = " + str(light_votes)
    print "water_votes = " + str(water_votes)
    print "total_votes = " + str(total_votes)

    if water_votes > 0:
        pump_water(5)

    light_votes = 1
    if light_votes > 0:
        call(['python3 /home/pi/Documents/plaeddit/lightOn.py'], shell=True)
    elif light_votes <= 0:
        call(['python3 /home/pi/Documents/plaeddit/lightOff.py'], shell=True)
