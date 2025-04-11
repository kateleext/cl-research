# List of subreddits to scrape
SUBREDDITS = [
    'hockey',
    'collegehockey',
    'nhl',
    'ushl',
]

# Search terms to look for in posts
SEARCH_TERMS = [
    # General USHL / Junior Hockey terms
    "USHL", "junior hockey", "Tier 1",

    # High-signal team names (no ambiguity)
    "Chicago Steel", "Youngstown Phantoms", "Fargo Force", "Dubuque Fighting Saints",
    "Tri-City Storm", "Waterloo Black Hawks", "Sioux Falls Stampede",

    # Fan-used shorthands (with low ambiguity risk)
    "Steel game", "Phantoms game", "Force game", "Fighting Saints", "Tri-City", "Waterloo", "Stampede",

    # Carefully selected partials or ambiguous tags with context
    "Muskegon Jacks", "Gamblers hockey", "Lincoln Stars USHL", "CR RoughRiders", "RoughRiders hockey"
]

# Number of days of historical data to scrape
DAYS_TO_SCRAPE = 90
