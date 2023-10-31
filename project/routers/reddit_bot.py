import praw
import time
import os
from project.llm import llm
import project.common as common
from project.routers.movie import get_movie
import asyncio

USERNAME = os.environ.get("REDDIT_USERNAME")
# Authenticate with Reddit
reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
    password=os.environ.get("REDDIT_PASSWORD"),
    user_agent='forgotmoviebot',
    username=os.environ.get("REDDIT_USERNAME")
)

if os.environ.get('ENV') == 'dev':
    from unittest import mock
    reddit = mock.MagicMock()
    reddit.subreddit = mock.MagicMock()
    reddit.subreddit.new = mock.MagicMock()
    fake_post = mock.MagicMock()
    fake_post.title = "That star wars where anakin races pods?"
    fake_post.selftext = "title"
    fake_post.saved = False
    reddit.subreddit('whatisthatmovie').new.return_value = [fake_post]
    common.write_notification = mock.MagicMock()
    llm = mock.MagicMock()
    llm.return_value = "Test Response"

from urllib.parse import quote_plus, urlencode
import urllib

def create_search_link(title, body):
    description = title + " " + body
    encoded_description = urlencode({'description':description})
    print(encoded_description)
    base_url = "https://forgotmoviesearch.com/search?"
    return base_url + encoded_description

async def do_subreddit(name, filter=True, limit=3):
        subreddit = reddit.subreddit(name)
        print('Fetching new posts')
        for post in subreddit.new(limit=limit):
            if filter:
                 if '[movie]' not in post.title.lower():
                      continue
            if not post.saved:  # check if the bot hasn't already replied to this post
                search_link = create_search_link(post.title, post.selftext)
                movie_name = get_movie(post.title + " " + post.selftext, llm=llm)
                response = f'''"{movie_name}"?
                
____
^^(I made forgotmoviesearch.com for questions like this. I put this post into the movie search: )^[here]({search_link}).
                
^^(mods lmk if you have any opinions on this. its somewhere between normal answer and ai generated.)'''

                # response = llm(response, system="Minorly reword the provided comment for reddit. Don't change it too much though. Only change a word or two.")

                common.write_notification(f"Responding to post: {post.title} with {response}")
                
                # Add a reply to the post
                post.reply(response)
                
                # Mark the post as saved (or processed)
                post.save()
                print('Replied to post')
                await asyncio.sleep(30)

async def respond_to_posts_forever():
    # Fetch the newest posts
    while True:
        await do_subreddit('whatisthatmovie', filter=False)
        await do_subreddit('tipofmytongue', limit=3)
        await asyncio.sleep(300)

async def get_my_past_10_comments_then_delete_negative_scored():
    while True:
        for comment in reddit.redditor(USERNAME).comments.new(limit=20):
            if comment.score < 0:
                comment.delete()
        await asyncio.sleep(600)
