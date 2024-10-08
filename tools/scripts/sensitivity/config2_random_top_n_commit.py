import os
import random
import pandas as pd


def select_random_commits(directory):
    for filename in os.listdir(directory):
        # Check if CSV file
        if filename.endswith('.csv'):
            # Construct the full file path
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            # Delete the last row
            df = df.drop(df.index[-1])
            # Select the first column
            first_column = df['Commit_Hash']
            # Randomly select a value 
            seed_value = 42
            random.seed(seed_value)
            #num_items_to_select = random.choice([1, 2])
            commits = random.sample(list(first_column.values), 1)
            print(filename)
            print(commits)


if __name__ == "__main__":
    select_random_commits('library_commit_stats')
