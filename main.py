import time

import telegram
import praw
from peewee import SqliteDatabase, Model, CharField

from settings import (TELEGRAM_ACCESS_TOKEN, TELEGRAM_CHANNEL_ID,
                      REDDIT_APP_KEY, REDDIT_APP_SECRET, REDDIT_USER_AGENT)

bot = telegram.Bot(token=TELEGRAM_ACCESS_TOKEN)
reddit_client = praw.Reddit(user_agent=REDDIT_USER_AGENT,
                            client_id=REDDIT_APP_KEY,
                            client_secret=REDDIT_APP_SECRET)
db = SqliteDatabase('wutong.db')


class FetchedThreads(Model):
    thread_id = CharField(unique=True)
    title = CharField()
    url = CharField()

    class Meta:
        database = db


def initialize_db():
    db.connect()
    # Create table only if it doesn't exist
    db.create_tables([FetchedThreads, ], safe=True)


def deinit():
    db.close()


def mark_thread_posted(thread_id, title, url):
    thread = {
        'thread_id': thread_id,
        'title': title,
        'url': url
    }
    FetchedThreads.create(**thread)


def is_thread_posted(thread_id):
    return FetchedThreads.select().where(FetchedThreads.thread_id == thread_id)


def post_image_to_tg(image_url, caption=''):
    # telegram restricts max characters of `caption` to be 200
    bot.send_photo(chat_id=TELEGRAM_CHANNEL_ID, photo=image_url,
                   caption=caption[:200])


def post_stuff_from_reddit(subreddit_name='gentlemanboners'):
    for submission in reddit_client.subreddit(subreddit_name).hot():
        if not submission.post_hint == 'image':
            continue
        thread_id = submission.id
        image_url = submission.url
        caption = submission.title
        if is_thread_posted(thread_id=thread_id):
            break
        post_image_to_tg(image_url=image_url, caption=caption)
        mark_thread_posted(thread_id=thread_id, url=image_url, title=caption)
        # sleep for 1 seconds
        # let me be nice to Telegram ^_^
        time.sleep(1)


def main():
    while True:
        post_stuff_from_reddit()
        # sleep for five minutes
        time.sleep(60 * 5)


if __name__ == '__main__':
    initialize_db()
    main()
    deinit()
