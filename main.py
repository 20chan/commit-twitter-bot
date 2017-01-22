import tweepy
import datetime
from random import choice
from time import sleep
from github import Github
usr_name = '@adnim'

f = open('key.config')
cons_key, cons_sec, tok_key, tok_sec, github_id, github_pw = f.read().split()
auth = tweepy.OAuthHandler(cons_key, cons_sec)
auth.set_access_token(tok_key, tok_sec)
api = tweepy.API(auth)

user = Github(github_id, github_pw)

msg_list = open('messages.txt', encoding='utf-8-sig').read().split('\n')

def tweet(msg):
    api.update_status(msg)

def today():
    t = datetime.datetime.today()
    t_d = datetime.datetime(t.year, t.month, t.day)
    return t_d - datetime.timedelta(hours=9)

def get_today_commits():
    for event in user.get_events():
        if event.created_at > today():
            if event.type in ['PushEvent', 'PullRequestEvent', 'IssueEvent']:
                yield event
        else:
            break

def handle():
    #if len(list(get_today_commits())) == 0:
        tweet(usr_name + ' ' + choice(msg_list))
        print('Tweet sent!')

while True:
    if today().hour > 14:
        handle()
    sleep(30)
