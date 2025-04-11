import pandas as pd
import os
from pathlib import Path

def deduplicate_reddit_data(input_file='reddit_data.csv', output_file='reddit_data_unique.csv'):
    """
    Deduplicates Reddit data based on post IDs and sorts by creation date.
    Preserves all comments while ensuring each post appears only once.
    """
    try:
        # Read the input file
        print(f"Reading data from {input_file}...")
        df = pd.read_csv(input_file)
        
        # Convert created_utc to datetime if it's not already
        if not pd.api.types.is_datetime64_any_dtype(df['created_utc']):
            df['created_utc'] = pd.to_datetime(df['created_utc'])
        
        # Get unique posts (where is_comment is False)
        posts_df = df[~df['is_comment']].drop_duplicates(subset=['post_id'])
        
        # Get all comments
        comments_df = df[df['is_comment']]
        
        # Combine unique posts with all comments
        unique_df = pd.concat([posts_df, comments_df])
        
        # Sort by creation date
        unique_df = unique_df.sort_values('created_utc', ascending=False)
        
        # Save to new file
        unique_df.to_csv(output_file, index=False)
        
        # Print statistics
        print("\nDeduplication complete!")
        print(f"Original file: {len(df):,} total records")
        print(f"Unique posts: {len(posts_df):,}")
        print(f"Total comments: {len(comments_df):,}")
        print(f"New file: {len(unique_df):,} total records")
        print(f"Saved to {output_file}")
        
        # Print some additional statistics
        print("\nAdditional Statistics:")
        print(f"Posts per subreddit:")
        print(posts_df['subreddit'].value_counts())
        print(f"\nComments per subreddit:")
        print(comments_df['subreddit'].value_counts())
        print(f"\nPosts per search term:")
        print(posts_df['search_term'].value_counts())
        
        return unique_df
        
    except Exception as e:
        print(f"Error during deduplication: {str(e)}")
        return None

if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set input and output paths
    input_path = os.path.join(script_dir, 'data', 'reddit_data.csv')
    output_path = os.path.join(script_dir, 'data', 'reddit_data_unique.csv')
    
    # Run deduplication
    deduplicate_reddit_data(input_path, output_path) 