#!/usr/bin/env python2
# coding=utf-8

# Copyright 2016 Delin <delin@delin.pro>


import json
import os
import re
import time

import oauth2

CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY', "")
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET', "")
TOKEN_KEY = os.environ.get('TWITTER_TOKEN_KEY', "")
TOKEN_SECRET = os.environ.get('TWITTER_TOKEN_SECRET', "")
YOUR_NIKNAME = os.environ.get('TWITTER_YOUR_NIKNAME', "delin")


def print_errors(errors):
    for error in errors:
        print u'\033[31m[error][{code}] {message}\033[0m'.format(code=error["code"], message=error["message"])


def get_tweets(count=100, since_id=1):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=TOKEN_KEY, secret=TOKEN_SECRET)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(
        "https://api.twitter.com/1.1/statuses/home_timeline.json?count=%d&since_id=%d" % (count, since_id),
        method="GET"
    )

    try:
        json_tweets = json.loads(content)
    except ValueError as error:
        errors = {
            "code": 0,
            "message": error,
        }
        print_errors(errors)
        return None

    if "errors" in json_tweets:
        print_errors(json_tweets["errors"])
        return None

    return json_tweets


def print_tweets(tweets):
    if len(tweets) > 0:
        print u'\n\033[90m----------------\033[0m'

    for tweet in reversed(tweets):
        nick = tweet['user']['screen_name']
        text = tweet['text']
        date = tweet['created_at']

        spaces_count = 16 - len(nick)
        if spaces_count < 0:
            spaces_count = 0
            nick = nick[:15] + "…"
        spaces = " ".ljust(spaces_count)

        text = re.sub(r'(#(?u)\w+)()', r'\033[93m\1\033[0m\2', text)
        text = re.sub(r'(@(?u)\w+)()', r'\033[94m\1\033[0m\2', text)
        text = re.sub(r'(@(?u)%s)()' % YOUR_NIKNAME, r'\033[92m\1\033[0m\2', text)

        print
        print u'\033[34m@{nick}{spaces}\033[90m \033[90m// {date}\033[0m'.format(nick=nick, spaces=spaces, date=date)
        print u'\t\033[0m{text}'.format(text=text)


since_id = 1

while True:
    tweets = get_tweets(since_id=since_id)

    if tweets:
        sleep_time = 60
        print_tweets(tweets)
        since_id = int(tweets[0]['id'])
    else:
        sleep_time = 120

    time.sleep(sleep_time)
