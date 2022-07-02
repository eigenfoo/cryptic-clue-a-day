import re
import pandas as pd


def extract_clue(tweet_text):
    x = [
        line
        for line in tweet_text.split("\n")
        if re.match(r".+\([0-9,'\- ]+\).*$", line)
    ]
    if len(x) != 1:
        return None
    return x[0].strip()


df = pd.read_json("raw_tweets.jsonl", lines=True, orient="records")
df["clue"] = df["clue_tweet_text"].apply(extract_clue)
df = df.assign(
    explanation=df["explanation_tweet_text"].str.strip(),
    clue_created_at=df["clue_tweet_created_at"],
    explanation_created_at=df["explanation_tweet_created_at"],
    clue_url="https://twitter.com/stellaphone/status/"
    + df["clue_tweet_id"].astype(str),
    explanation_url="https://twitter.com/stellaphone/status/"
    + df["explanation_tweet_id"].astype(str),
)

(
    df[
        [
            "clue",
            "explanation",
            "clue_url",
            "explanation_url",
            "clue_created_at",
            "explanation_created_at",
        ]
    ]
    .dropna()
    .sort_values("clue_created_at", ascending=False)
    .to_csv("cryptic_clue_a_day.csv", index=False)
)
