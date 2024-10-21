import pandas as pd
import os


def process_mean_coverage(input_directory, output_file):
    # List to hold mean results
    mean_results = []

    # Iterate through all files in the input directory
    for file_name in os.listdir(input_directory):
        # Construct the full file path
        file_path = os.path.join(input_directory, file_name)
        
        # Check if it is a file (and not a subdirectory)
        if os.path.isfile(file_path):
            # Read the file into a DataFrame
            try:
                df = pd.read_csv(file_path)
                print(f"Processing file: {file_name}")
                print(df)  # Print the DataFrame
                
                # Handle NaN values before stripping '%' and converting to float
                for col in ['Cover', 'Cover.1', 'Cover.2']:
                    if col in df.columns:
                        # Replace NaN values with an empty string or '0%'
                        df[col] = df[col].fillna('0%')
                        # Strip '%' from the strings and convert to float
                        df[col] = df[col].str.rstrip('%').astype(float)
                
                # Compute the mean for the DataFrame
                mean_values = df.mean(numeric_only=True)
                mean_values['File'] = file_name  # Add the filename to the mean results
                
                # Append the mean results to the list
                mean_results.append(mean_values)
            
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    # Convert mean results to a DataFrame
    mean_results_df = pd.DataFrame(mean_results)

    # Save the mean results to a CSV file
    mean_results_df.to_csv(output_file, index=False)

    print(f"Mean results saved to {output_file}.")


if __name__ == "__main__":
    process_mean_coverage("/home/mhuang/research/ContinuousFuzzBench/tools/scripts/evaluation/log/aflgo/target-file-coverage", "./log/aflgo/coverage-aflgo-experiments-mean-file-coverage")

