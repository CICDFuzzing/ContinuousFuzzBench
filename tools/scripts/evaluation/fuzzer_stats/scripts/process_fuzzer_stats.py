import pandas as pd
import os

def process_libfuzzer_mean_fuzzer_stats(input_directory, output_file):
    mean_results = []

    for file_name in os.listdir(input_directory):
        file_path = os.path.join(input_directory, file_name)
        if os.path.isfile(file_path):
            try:
                df = pd.read_csv(file_path)
                print(f"Processing file: {file_name}")
                print(df) 
                df['exec_speed'] = df['execs_done'] / df['runtime']
                mean_values = df.mean(numeric_only=True)

                file_name_parts = file_name.split('_')
                fuzzer_name = file_name_parts[0]                
                target_name = "_".join(file_name_parts[1:4])      

                mean_values['FUZZER'] = fuzzer_name  
                mean_values['TARGET'] = target_name
                mean_results.append(mean_values)
            
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
    col_names=['FUZZER', 'TARGET', 'runtime', 'execs_done', 'exec_speed', 'unique_crashes', 'oom', 'timeout']
    mean_results_df = pd.DataFrame(mean_results, columns=col_names)
    print(mean_results_df)

    mean_results_df.to_csv(output_file, index=False, float_format='%.2f')

    print(f"Mean results saved to {output_file}.")

    return mean_results


def process_mean_fuzzer_stats(input_directory, output_file):
    mean_results = []

    for file_name in os.listdir(input_directory):
        file_path = os.path.join(input_directory, file_name)
        if os.path.isfile(file_path):
            try:
                df = pd.read_csv(file_path, names=['start_time', 'last_update', 'execs_done', 'unique_crashes'], header=None)
                print(f"Processing file: {file_name}")
                print(df) 

                df['runtime'] = df['last_update'] - df['start_time']
                df['exec_speed'] = df['execs_done'] / df['runtime']
                df.drop(columns=['start_time', 'last_update'], inplace=True)
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
    col_names=['FUZZER', 'TARGET', 'PROGRAM', 'runtime', 'execs_done', 'exec_speed', 'unique_crashes']
    mean_results_df = pd.DataFrame(mean_results, columns=col_names)
    print(mean_results_df)

    mean_results_df.to_csv(output_file, index=False, float_format='%.2f')

    print(f"Mean results saved to {output_file}.")

    return mean_results


if __name__ == "__main__":
    #process_mean_fuzzer_stats('/home/mhuang/research/thesis/scratch-dir/log/fuzzer_stats/ffd', '/home/mhuang/research/thesis/scratch-dir/log/fuzzer_stats/ffd_fuzzer_stats')
    process_libfuzzer_mean_fuzzer_stats('/home/mhuang/research/thesis/scratch-dir/log/fuzzer_stats/libfuzzer', '/home/mhuang/research/thesis/scratch-dir/log/fuzzer_stats/libfuzzer_fuzzer_stats')
