import tweepy
import datetime
import os
from random import choice
from time import sleep, time
from github import Github
usr_name = '@0xadnim'

def get_infos():
    return os.environ.get('cons_key'), os.environ.get('cons_sec'), os.environ.get('tok_key'), os.environ.get('tok_sec'), os.environ.get('github_id'), os.environ.get('github_pw')

cons_key, cons_sec, tok_key, tok_sec, github_id, github_pw = get_infos()
auth = tweepy.OAuthHandler(cons_key, cons_sec)
auth.set_access_token(tok_key, tok_sec)
api = tweepy.API(auth, wait_on_rate_limit=True)

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
    api.update_status(usr_name + ' 오늘 총 ' + str(len(list(get_today_commits()))) +'커밋을 했어요!', id)

class mentionListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)
        send_log(status.id)

if __name__ == '__main__':
    tweet('Start Running Bot! ..At ' + str(time()) + '!')
    mlistener = mentionListener()
    stream = tweepy.Stream(auth=api.auth, listener=mlistener)
    stream.filter(track=['dailycommit_bot'])
    lastId = -1
    while True:
        if today().hour > 14:
            handle()
        sleep(1200)
