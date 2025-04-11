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
    Analyzes Reddit posts and comments using OpenAI's API to extract multiple behavioral episodes per entry.
    Truncates input if too long to avoid token limits.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'data', data_file)

    df = pd.read_csv(data_path)
    if max_rows is not None:
        df = df.head(max_rows)

    all_results = []

    print("Processing entries for multi-decision extraction...")
    for index, row in df.iterrows():
        print(f"Processing {index+1}/{len(df)}...")
        try:
            combined_content = row['text']
            truncated_content = combined_content[:MAX_INPUT_CHARS]

            input_messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": truncated_content}
            ]

            response = client.responses.create(
                model="gpt-4o-2024-08-06",
                input=input_messages,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "multi_decision_analysis",
                        "schema": drivers_schema,
                        "strict": False
                    }
                }
            )

            parsed = json.loads(response.output_text)
            episodes = parsed.get("episodes", [])
            for ep in episodes:
                ep["post_id"] = row.get("post_id")
                ep["subreddit"] = row.get("subreddit") 
                ep["post_url"] = f"https://www.reddit.com/r/{row.get('subreddit')}/comments/{row.get('post_id')}"
                ep["post_title"] = row.get("title")
                ep["text"] = row.get("text")
            all_results.extend(episodes)

        except Exception as e:
            print(f"Error on row {index}: {str(e)}")
            continue

    if all_results:
        output_df = pd.DataFrame(all_results)
        output_path = os.path.join(script_dir, 'data', 'analysis_results.csv')
        output_df.to_csv(output_path, index=False)
        print(f"Analysis complete. Exported {len(output_df)} episodes to {output_path}")
        return output_df
    else:
        print("No qualifying entries extracted.")
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


