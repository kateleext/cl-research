# scrape.py — treats each comment as its own row
import praw
import pandas as pd
import os
from datetime import datetime, timedelta
from .specs import SUBREDDITS, SEARCH_TERMS, POSTS_PER_SUBREDDIT, DAYS_TO_SCRAPE
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

def scrape_reddit():
    """
    Scrapes posts and comments from r/chicago and r/AskChicago that match the search terms.
    Returns a DataFrame with post and comment data.
    """
    records = []
    cutoff_date = datetime.utcnow() - timedelta(days=DAYS_TO_SCRAPE)

    for subreddit_name in SUBREDDITS:
        print(f"Searching r/{subreddit_name}...")
        subreddit = reddit.subreddit(subreddit_name)

        for term in SEARCH_TERMS:
            print(f"  Searching for: {term}")
            term_posts = 0
            term_comments = 0
            try:
                # Search posts in the subreddit
                for submission in subreddit.search(term, time_filter='all', limit=POSTS_PER_SUBREDDIT):
                    if datetime.fromtimestamp(submission.created_utc) < cutoff_date:
                        continue

                    term_posts += 1
                    # Add the post itself
                    records.append({
                        'post_id': submission.id,
                        'subreddit': subreddit_name,
                        'title': submission.title,
                        'text': submission.selftext,
                        'created_utc': datetime.fromtimestamp(submission.created_utc),
                        'score': submission.score,
                        'is_comment': False,
                        'url': f"https://www.reddit.com/r/{subreddit_name}/comments/{submission.id}",
                        'parent_url': None,
                        'search_term': term
                    })

                    # Add comments from the post
                    submission.comments.replace_more(limit=0)  # Remove MoreComments objects
                    for comment in submission.comments.list():
                        if datetime.fromtimestamp(comment.created_utc) < cutoff_date:
                            continue

                        term_comments += 1
                        records.append({
                            'post_id': comment.id,
                            'subreddit': subreddit_name,
                            'title': None,  # Comments don't have titles
                            'text': comment.body,
                            'created_utc': datetime.fromtimestamp(comment.created_utc),
                            'score': comment.score,
                            'is_comment': True,
                            'url': f"https://www.reddit.com/r/{subreddit_name}/comments/{submission.id}/comment/{comment.id}",
                            'parent_url': f"https://www.reddit.com/r/{subreddit_name}/comments/{submission.id}",
                            'search_term': term
                        })

                print(f"    Found {term_posts} posts and {term_comments} comments for '{term}'")

            except Exception as e:
                print(f"Error searching for '{term}' in r/{subreddit_name}: {str(e)}")
                continue

    df = pd.DataFrame(records)
    return df

def save_to_csv(df, filename='reddit_data.csv'):
    """
    Saves the DataFrame to a CSV file in the data directory.
    Creates the directory if it doesn't exist.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    filepath = os.path.join(data_dir, filename)
    df.to_csv(filepath, index=False)
    print(f"Saved {len(df)} records to {filepath}")

if __name__ == "__main__":
    df = scrape_reddit()
    save_to_csv(df)

