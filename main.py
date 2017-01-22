import tweepy
import datetime

f = open('key.config')
cons_key, cons_sec, tok_key, tok_sec = f.read().split()
auth = tweepy.OAuthHandler(cons_key, cons_sec)
auth.set_access_token(tok_key, tok_sec)
api = tweepy.API(auth)

def tweet(msg):
    api.update_status(msg)

def get_today_commits(user):
    today = datetime.datetime.today()
    today_date = datetime.datetime(today.year, today.month, today.day)
    today_date_ko = today_date - datetime.timedelta(hours=9)

    for event in user.get_events():
        if event.created_at > today_date_ko:
            if event.type in ['PushEvent', 'PullRequestEvent', 'IssueEvent']:
                yield event
        else:
            break
