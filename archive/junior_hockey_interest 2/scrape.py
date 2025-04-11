# scrape.py — treats each comment as its own row
import praw
import pandas as pd
import os
from datetime import datetime, timedelta
from .specs import SUBREDDITS, SEARCH_TERMS, DAYS_TO_SCRAPE
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def scrape_reddit():
    """
    Scrapes Reddit posts and all comments as individual behavioral units.
    Returns a DataFrame with post and comment-level entries.
    """
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT')
    )

    records = []
    seen_post_ids = set()  # Track unique post IDs

    for subreddit in SUBREDDITS:
        print(f"Checking subreddit: r/{subreddit}")
        try:
            sub = reddit.subreddit(subreddit)

            for search_term in SEARCH_TERMS:
                print(f"  Searching for: '{search_term}'")
                time_filter = datetime.now() - timedelta(days=DAYS_TO_SCRAPE)

                for post in sub.search(search_term, limit=100):
                    if datetime.fromtimestamp(post.created_utc) <= time_filter:
                        continue

                    # Skip if we've already seen this post
                    if post.id in seen_post_ids:
                        continue
                    seen_post_ids.add(post.id)

                    # Main post as row
                    records.append({
                        'type': 'post',
                        'post_id': post.id,
                        'parent_id': None,
                        'comment_id': None,
                        'subreddit': subreddit,
                        'search_term': search_term,
                        'title': post.title,
                        'text': post.selftext,
                        'author': str(post.author),
                        'score': post.score,
                        'created_utc': datetime.fromtimestamp(post.created_utc),
                    })

                    # Comments as separate rows
                    post.comments.replace_more(limit=None)
                    for comment in post.comments.list():
                        records.append({
                            'type': 'comment',
                            'post_id': post.id,
                            'parent_id': comment.parent_id,
                            'comment_id': comment.id,
                            'subreddit': subreddit,
                            'search_term': search_term,
                            'title': post.title,
                            'text': comment.body,
                            'author': str(comment.author),
                            'score': comment.score,
                            'created_utc': datetime.fromtimestamp(comment.created_utc),
                        })

        except Exception as e:
            print(f"Error scraping r/{subreddit}: {str(e)}")

    # Convert to DataFrame and save
    df = pd.DataFrame(records)
    
    # Sort by creation date
    df = df.sort_values('created_utc', ascending=False)
    
    # Save to CSV
    output_path = 'reddit_data.csv'
    df.to_csv(output_path, index=False)
    print(f"\nScraping complete!")
    print(f"Found {len(seen_post_ids)} unique posts")
    print(f"Total records (posts + comments): {len(df)}")
    print(f"Saved to {output_path}")
    
    return df

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    df = scrape_reddit()
    df.to_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'reddit_data.csv'), index=False)
    print(f"Saved {len(df)} rows to data/reddit_data.csv")
