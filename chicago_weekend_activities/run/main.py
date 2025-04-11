import pandas as pd
from ..analyze import analyze_data
import os
import sys

def main():
    """
    Run analysis on the full dataset
    """
    # Get path to data directory relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up one level to reach the parent directory that contains both 'run' and 'data' folders
    template_dir = os.path.dirname(script_dir)

    # Build the path to the data file
    data_path = os.path.join(template_dir, 'data', 'reddit_data.csv')
    
    # Load the data
    df = pd.read_csv(data_path)
        
    # Run analysis
    print("\nRunning analysis on full dataset...")
    results = analyze_data()
    
    return results

if __name__ == "__main__":
    main()
