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
        already_seen = False
        if comment.author == "AggieBot":
            continue

        # check to see if I have replied to the comment already
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


def parse_comment(text):
    ''' this function takes in a string representing the body of a comment and 
    returns either a 1 symbolizing `water` or a -1 symbolizing `not water` '''

    previous_word = ""
    for word in text.split():
        if word == "water":
            return -1 if previous_word == "no" else 1
        previous_word = word

#make_daily_post()
#get_todays_post()

print parse_comment("this is a long comment that will eventually say water and then end")
