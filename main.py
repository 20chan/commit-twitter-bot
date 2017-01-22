import tweepy
import datetime
import os
from random import choice
from time import sleep, time
from github import Github
usr_name = '@adnim'

def get_infos():
    return os.environ.get('cons_key'), os.environ.get('cons_sec'), os.environ.get('tok_key'), os.environ.get('tok_sec'), os.environ.get('github_id'), os.environ.get('github_pw')

cons_key, cons_sec, tok_key, tok_sec, github_id, github_pw = get_infos()
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
    for event in user.get_user().get_events():
        if event.created_at > today():
            if event.type in ['PushEvent', 'PullRequestEvent', 'IssueEvent']:
                yield event
        else:
            break

def handle():
    if len(list(get_today_commits())) == 0:
        try:
            tweet(usr_name + ' ' + choice(msg_list))
        except tweepy.error.TweepError:
            print('Tweet duplicated')
            pass
        print('Tweet sent!')

def send_log(id):
    api.update_status('오늘 총 ' + str(len(list(get_today_commits()))) +'커밋을 했어요!', id)

if __name__ == '__main__':
    tweet('Start Running Bot! ..At ' + str(time()) + '!')
    lastId = -1
    while True:
        if today().hour > 14:
            handle()
        lm = api.mentions_timeline(count=1)[0]
        if lm.user.screen_name == usr_name and lm.id != lastId:
            lastId = lm.id
            send_log(lastId)

        sleep(1)
