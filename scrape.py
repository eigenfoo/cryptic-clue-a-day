import os
import re
import json
import requests
import tweepy


bearer_token = os.environ["TWITTER_API_BEARER_TOKEN"]
client = tweepy.Client(bearer_token)

recent_tweets = client.search_recent_tweets(
    query="(#explanationfriday) (from:stellaphone)",
    tweet_fields="created_at",
).data

# Uncomment this to backfill from a .txt file of tweet ids
# with open("backfill_tweet_ids.txt") as f:
#     tweet_ids = list(map(int, f.read().split()))
# recent_tweets.extend(client.get_tweets(tweet_ids, tweet_fields="created_at").data)

for explanation_tweet in recent_tweets:
    # Assume the last t.co link is the retweet with the clue.
    twitter_short_urls = re.findall(r"https://t\.co/\w+", explanation_tweet.text)
    if not twitter_short_urls:
        continue

    clue_url = requests.get(twitter_short_urls[-1]).url
    clue_tweet_id = int(re.search(r"[0-9]+$", clue_url).group())
    clue_tweet = client.get_tweet(clue_tweet_id, tweet_fields="created_at")

    d = {
        "clue_tweet_id": clue_tweet_id,
        "clue_tweet_text": clue_tweet.data.text,
        "clue_tweet_created_at": clue_tweet.data.created_at.strftime("%Y-%m-%d %T%z"),
        "explanation_tweet_id": explanation_tweet.id,
        "explanation_tweet_text": explanation_tweet.text,
        "explanation_tweet_created_at": explanation_tweet.created_at.strftime(
            "%Y-%m-%d %T%z"
        ),
    }
    with open("raw_tweets.jsonl", "a+") as f:
        json.dump(d, f)
        f.write("\n")
