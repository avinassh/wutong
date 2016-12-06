import telegram
import praw

from settings import (TELEGRAM_ACCESS_TOKEN, TELEGRAM_CHANNEL_ID,
                      REDDIT_APP_KEY, REDDIT_APP_SECRET, REDDIT_USER_AGENT)

bot = telegram.Bot(token=TELEGRAM_ACCESS_TOKEN)
reddit_client = praw.Reddit(user_agent=REDDIT_USER_AGENT,
                            client_id=REDDIT_APP_KEY,
                            client_secret=REDDIT_APP_SECRET)


def post_image_to_tg(image_url, caption=''):
    # telegram restricts max characters of `caption` to be 200
    bot.send_photo(chat_id=TELEGRAM_CHANNEL_ID, photo=image_url,
                   caption=caption[:200])


def get_stuff_from_reddit(subreddit='gentlemanboners'):
    for submission in reddit_client.subreddit(subreddit).new():
        if submission.post_hint == 'image':
            post_image_to_tg(image_url=submission.url,
                             caption=submission.title)


def main():
    pass


if __name__ == '__main__':
    get_stuff_from_reddit()
