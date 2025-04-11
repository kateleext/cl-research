# analyze.py (multi-decision compatible with wrapped schema and input truncation)
import pandas as pd
import json
from openai import OpenAI
from datetime import datetime
from .prompts import system_message, drivers_schema
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

MAX_INPUT_CHARS = 10000

def analyze_data(max_rows=None, data_file='reddit_data.csv'):
    """
    Analyzes Reddit posts and comments about weekend activities in Chicago.
    Identifies decision-making patterns and factors influencing activity choices.
    Handles both posts and comments, maintaining their relationships.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'data', data_file)

    df = pd.read_csv(data_path)
    if max_rows is not None:
        df = df.head(max_rows)

    all_results = []
    qualified_count = 0

    print("Processing entries for weekend activity analysis...")
    for index, row in df.iterrows():
        print(f"Processing {index+1}/{len(df)}...")
        try:
            # Prepare the content for analysis
            content = row['text']
            if pd.isna(content) or not content.strip():
                continue

            # For comments, include context about it being a comment
            if row['is_comment']:
                content = f"[Comment in response to post: {row['parent_url']}]\n\n{content}"
            else:
                content = f"[Original post: {row['url']}]\n\n{content}"

            truncated_content = content[:MAX_INPUT_CHARS]

            input_messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": truncated_content}
            ]

            response = client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=input_messages,
                response_format={"type": "json_object"},
                functions=[{
                    "name": "analyze_weekend_activities",
                    "description": "Analyze weekend activity decisions and their influencing factors",
                    "parameters": drivers_schema
                }],
                function_call={"name": "analyze_weekend_activities"}
            )

            parsed = json.loads(response.choices[0].message.function_call.arguments)
            episodes = parsed.get("episodes", [])
            
            if episodes:
                qualified_count += 1
                print(f"\n✅ Found qualified entry #{qualified_count} in row {index+1}:")
                print(f"Source: {'Comment' if row['is_comment'] else 'Post'} in r/{row['subreddit']}")
                print(f"URL: {row['url']}")
                if row['is_comment']:
                    print(f"Parent Post: {row['parent_url']}")
                print("\nExtracted Episodes:")
                
                for i, ep in enumerate(episodes, 1):
                    print(f"\nEpisode {i}:")
                    print(f"Context: {ep['decision_context']}")
                    print(f"Activity Type: {ep['activity_type']}")
                    print(f"Final Choice: {ep['final_choice']}")
                    print(f"Decision Factors: {', '.join(ep['decision_factors'])}")
                    if 'reasoning' in ep:
                        print(f"Reasoning: {ep['reasoning']}")
                    print("-" * 50)
            
            for ep in episodes:
                # Add metadata about the source
                ep["source_id"] = row['post_id']
                ep["source_type"] = "comment" if row['is_comment'] else "post"
                ep["subreddit"] = row['subreddit']
                ep["source_url"] = row['url']
                ep["score"] = row['score']
                ep["created_utc"] = row['created_utc']
                
                # Add parent post information for comments
                if row['is_comment']:
                    ep["parent_post_url"] = row['parent_url']
                
                # Add the original content for reference
                ep["original_content"] = row['text']
                
            all_results.extend(episodes)

        except Exception as e:
            print(f"❌ Error on row {index+1}: {str(e)}")
            continue

    if all_results:
        output_df = pd.DataFrame(all_results)
        output_path = os.path.join(script_dir, 'data', 'weekend_activity_analysis.csv')
        output_df.to_csv(output_path, index=False)
        print(f"\nAnalysis complete. Found {qualified_count} qualified entries with {len(output_df)} total episodes.")
        print(f"Results exported to {output_path}")
        return output_df
    else:
        print("\nNo qualifying entries extracted.")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            max_rows = int(sys.argv[1])
        except ValueError:
            print("Invalid max_rows value. Using all rows.")
            max_rows = None
    else:
        max_rows = None

    analyze_data(max_rows=max_rows)


