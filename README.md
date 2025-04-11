# Chicago Weekend Activities Twitter Analysis

This project collects and analyzes Twitter data related to weekend activities in Chicago. It uses the Twitter API to gather tweets and provides tools for analyzing engagement patterns and content trends.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your Twitter API credentials:
```
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

## Usage

### Data Collection

To collect tweets:
```bash
python -m twitter.scrape
```

### Analysis

To analyze collected tweets:
```bash
python -m twitter.analyze
```

## Project Structure

- `twitter/`: Main package directory
  - `scrape.py`: Twitter data collection script
  - `analyze.py`: Data analysis and visualization tools
  - `specs.py`: Configuration settings and search terms
- `requirements.txt`: Project dependencies
- `.env`: Twitter API credentials (not tracked by git)

## Features

- Collects tweets based on Chicago-specific search terms
- Analyzes tweet engagement metrics
- Generates visualizations of tweet patterns
- Handles rate limiting and error cases
- Saves data in CSV format for further analysis 