import pandas as pd
from ..analyze import analyze_data
import os
import sys

def test_analysis(n_rows=5):
    """
    Run analysis on first n rows of data as a test
    Args:
        n_rows (int): Number of rows to test. Defaults to 5.
    """
    # Load the data
    # Get path to data directory relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up one level to reach the parent directory that contains both 'run' and 'data' folders
    template_dir = os.path.dirname(script_dir)

# Build the path to the data file
    data_path = os.path.join(template_dir, 'data', 'reddit_data.csv')
    test_path = os.path.join(template_dir, 'data', 'test_data.csv')
    # Now use data_path to read your CSV
    df = pd.read_csv(data_path)
        
    # Take first n rows
    test_df = df.sample(n=n_rows)
    
    # Save test data
    test_df.to_csv(test_path, index=False)
    
    # Run analysis
    print(f"\nRunning test analysis on {n_rows} rows...")
    results = analyze_data(n_rows, data_file='test_data.csv')
    
    # Restore full dataset
    df.to_csv(data_path, index=False)
    return results

if __name__ == "__main__":
    # Get number of rows from command line arg, default to 5
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    test_analysis(n)

    
