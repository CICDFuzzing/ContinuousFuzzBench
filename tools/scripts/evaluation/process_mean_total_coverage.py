import pandas as pd
import os


def process_mean_total_coverage(input_directory, output_file):
    mean_results = []

    for file_name in os.listdir(input_directory):
        file_path = os.path.join(input_directory, file_name)
        if os.path.isfile(file_path):
            try:
                df = pd.read_csv(file_path)
                print(f"Processing file: {file_name}")
                print(df) 

                for col in ['Executed', 'Cover', 'Cover.1', 'Cover.2']:
                    if col in df.columns:
                        df[col] = df[col].fillna('0%')
                        df[col] = df[col].str.rstrip('%').astype(float)
                
                mean_values = df.mean(numeric_only=True)

                file_name_parts = file_name.split('_')
                fuzzer_name = file_name_parts[0]                
                target_name = "_".join(file_name_parts[1:4])      
                program_name = file_name_parts[4]      

                mean_values['FUZZER'] = fuzzer_name  
                mean_values['TARGET'] = target_name
                mean_values['PROGRAM'] = program_name
                mean_results.append(mean_values)
            
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    col_names = ['FUZZER', 'TARGET', 'PROGRAM', 'Regions', 'Missed_Regions', 'Cover', 'Functions', 'Missed_Functions', 'Executed', 'Lines', 'Missed_Lines', 'Cover.1', 'Branches', 'Missed_Branches', 'Cover.2']
    mean_results_df = pd.DataFrame(mean_results, columns=col_names)
    print(mean_results_df)

    mean_results_df.to_csv(output_file, index=False, float_format='%.3f')

    print(f"Mean results saved to {output_file}.")

    return mean_results


def process_mean_target_function_coverage(input_directory, output_file):

    mean_results = []

    for file_name in os.listdir(input_directory):
        file_path = os.path.join(input_directory, file_name)
        if os.path.isfile(file_path):
            try:
                df = pd.read_csv(file_path)
                print(f"Processing file: {file_name}")
                print(df)  
                
                for col in ['Cover', 'Cover.1', 'Cover.2']:
                    if col in df.columns:
                        df[col] = df[col].fillna('0%')
                        df[col] = df[col].str.rstrip('%').astype(float)
                
                mean_values = df.mean(numeric_only=True)

                file_name_parts = file_name.split('_')
                fuzzer_name = file_name_parts[0]                
                target_name = "_".join(file_name_parts[1:4])      
                program_name = file_name_parts[4]         
                target_function = df['Filename'].iloc[0]     

                mean_values['FUZZER'] = fuzzer_name  
                mean_values['TARGET'] = target_name
                mean_values['PROGRAM'] = program_name
                mean_values['Filename'] = target_function

                mean_results.append(mean_values)
            
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    col_names = ['FUZZER', 'TARGET', 'PROGRAM', 'Filename', 'Regions', 'Miss', 'Cover', 'Lines', 'Miss', 'Cover.1', 'Branches', 'Miss', 'Cover.2']
    mean_results_df = pd.DataFrame(mean_results, columns=col_names)
    print(mean_results_df)

    mean_results_df.to_csv(output_file, index=False, float_format='%.3f')

    print(f"Mean results saved to {output_file}.")

    return df


def sort_and_format_results(file_name):
    df = pd.read_csv(file_name)
    custom_order = ['libpng_4_1', 'libsndfile_2_1', 'libsndfile_7_1', 'libsndfile_15_1', 'libtiff_6_1', 'libtiff_7_1', 'libtiff_9_1', 'libtiff_10_1', 'libxml2_1_2', 'libxml2_2_1', 'libxml2_8_1', 'libxml2_10_2', 'libxml2_12_2', 'libxml2_14_1', 'libxml2_15_1', 'libxml2_16_1', 'libxml2_16_2', 'openssl_1_3', 'openssl_1_5', 'openssl_4_4', 'openssl_5_1', 'openssl_6_4', 'openssl_6_5', 'openssl_6_6', 'openssl_7_2', 'openssl_7_4', 'openssl_8_1', 'openssl_9_1', 'openssl_10_5', 'openssl_11_4', 'openssl_11_6', 'openssl_12_6', 'openssl_13_2', 'openssl_16_6', 'openssl_17_2', 'openssl_17_4', 'openssl_18_5', 'openssl_19_1', 'openssl_20_3', 'openssl_20_4', 'php_4_1', 'php_6_2', 'php_11_2', 'php_15_2', 'php_16_3', 'poppler_3_1', 'poppler_9_1', 'poppler_17_1', 'sqlite3_18_1', 'sqlite3_20_1']
    df['TARGET'] = pd.Categorical(df['TARGET'], categories=custom_order, ordered=True)
    df = df.sort_values('TARGET').reset_index(drop=True)
    # Format each row as "x & x & x & x & x \\"
    df = df[['TARGET', 'Lines', 'Cover.1', 'Branches', 'Cover.2']]
    #df = df[['TARGET', 'Functions', 'Executed', 'Lines', 'Cover.1', 'Branches', 'Cover.2']]
    # Escape underscores in the first column
    df['TARGET'] = df['TARGET'].str.replace('_', r'\_')
    #df['Filename'] = df['Filename'].str.replace('_', r'\_')
    formatted_rows = df.apply(
        lambda row: ' & '.join(f"{x:.2f}" if isinstance(x, (int, float)) else str(x) for x in row) + ' \\\\', 
        axis=1
    )

    # Print each formatted row
    for row in formatted_rows:
        print(row)
    return df
    
if __name__ == "__main__":
    for fuzzer in ['afl', 'aflpp', 'libfuzzer', 'aflgo', 'ffd']:
          print(fuzzer)
    #     process_mean_total_coverage("/home/huicongh/ContinuousFuzzBench/tools/scripts/evaluation/log/total_coverage/{}".format(fuzzer), "./log/mean_coverage/mean_total_coverage/{}_mean_total_coverage".format(fuzzer))
    #     process_mean_target_function_coverage("/home/huicongh/ContinuousFuzzBench/tools/scripts/evaluation/log/target_function_coverage/{}".format(fuzzer), "./log/mean_coverage/mean_target_function_coverage/{}_mean_target_function_coverage".format(fuzzer))
    #     sort_and_format_results('/home/huicongh/ContinuousFuzzBench/tools/scripts/evaluation/log/mean_coverage/mean_total_coverage/{}_mean_total_coverage'.format(fuzzer))
          sort_and_format_results('/home/huicongh/ContinuousFuzzBench/tools/scripts/evaluation/log/mean_coverage/mean_target_function_coverage/{}_mean_target_function_coverage'.format(fuzzer))
