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


if __name__ == "__main__":
    for fuzzer in ['afl', 'aflpp', 'aflgo', 'libfuzzer', 'ffd']:
        #process_mean_total_coverage("/home/huicongh/ContinuousFuzzBench/tools/scripts/evaluation/log/total_coverage/{}".format(fuzzer), "./log/mean_coverage/mean_total_coverage/{}_mean_total_coverage".format(fuzzer))
        process_mean_target_function_coverage("/home/huicongh/ContinuousFuzzBench/tools/scripts/evaluation/log/target_function_coverage/{}".format(fuzzer), "./log/mean_coverage/mean_target_function_coverage/{}_mean_target_function_coverage".format(fuzzer))
