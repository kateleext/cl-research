# Chicago Weekend Activities Research

This project analyzes Reddit discussions about weekend activities in Chicago to understand decision-making patterns and situational drivers behind activity choices.

## Project Overview

The research aims to:
- Identify common weekend activities in Chicago
- Understand factors influencing activity choices
- Analyze decision-making patterns
- Map temporal trends in activity planning
- Identify key situational drivers

## Data Collection

### Source
- Reddit posts and comments from r/chicago and r/AskChicago
- Focus on posts discussing weekend plans, activities, and recommendations

### Search Terms
- "weekend plans"
- "what to do"
- "friday night"
- "saturday"
- "going out"
- And other Chicago-specific activity terms

### Data Structure
Each record includes:
- Post/comment content
- Creation timestamp
- Subreddit
- Score (upvotes)
- Search term match
- Metadata (URLs, IDs)

## Analysis Methodology

### 1. Data Collection (`scrape.py`)
- Collects posts and comments from target subreddits
- Filters by search terms and date range
- Ensures unique posts (no duplicates)
- Saves to CSV format

### 2. Data Deduplication (`deduplicate.py`)
- Removes duplicate posts while preserving all comments
- Maintains data integrity
- Provides statistics on data distribution

### 3. LLM Analysis (`analyze.py`)
Uses OpenAI's GPT-4 to analyze each post/comment for:
- Decision context
- Activity type
- Influencing factors
- Sentiment
- Engagement level
- Activity context

### 4. Situational Drivers
Identifies key factors influencing decisions:
1. Social Bonding
2. Novelty/FOMO
3. Convenience
4. Cost/Value Sensitivity
5. Affective State
6. Weather-Driven
7. Out-of-Character Behavior
8. Peer Influence
9. Spontaneity
10. External Stimulus

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
OPENAI_API_KEY=your_openai_api_key
```

## Usage

1. Collect data:
```bash
python -m chicago_weekend_activities.scrape
```

2. Deduplicate data (if needed):
```bash
python -m chicago_weekend_activities.deduplicate
```

3. Run analysis:
```bash
python -m chicago_weekend_activities.analyze
```

## Output Files

- `data/reddit_data.csv`: Raw collected data
- `data/reddit_data_unique.csv`: Deduplicated data
- `data/analysis_results.csv`: LLM analysis results

## Project Structure

```
chicago_weekend_activities/
├── data/                   # Data storage
├── specs.py               # Configuration parameters
├── scrape.py              # Data collection
├── deduplicate.py         # Data cleaning
├── analyze.py             # LLM analysis
├── prompts.py             # LLM prompts and schemas
└── README.md              # Project documentation
```
