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
            elif vote == 0:
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

# --- Light Control ----
# Have to install some libraries first, look on:
# https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
import time
import board
import neopixel

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
# D18 is same as GPIO18 on board.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 256

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)

# Turn on light to all white, will stay on until turned off
# Comment this line out if you have RGBW/GRBW NeoPixels
pixels.fill((255, 255, 255))
pixels.show()

# -- End of Light Control ---

post = get_todays_post()

if post is not None:
    light_votes, water_votes, total_votes = tally_votes(get_todays_post())
    print "light_votes = " + str(light_votes)
    print "water_votes = " + str(water_votes)
    print "total_votes = " + str(total_votes)

    if water_votes > 0:
        pump_water(5)

    if light_votes > 0:
        call(['sudo python3 lightOn.py'], shell=True)
    elif light_votes <= 0:
        call(['sudo python3 lightOff.py'], shell=True)
