import pandas as pd
import os


def get_fuzzer_data(log_path):
    fuzzer_stats_col_names = ['fuzzer', 'library', 'fuzz_target', 'start_time', 'last_update', 'execs_done', 'execs_per_sec', 'unique_crashes', 'execs_since_crash', 'findings_path']
    fuzzer_df = pd.read_csv(log_path, header=None, names=fuzzer_stats_col_names)
    fuzzer_df['runtime'] = fuzzer_df['last_update'] - fuzzer_df['start_time']
    fuzzer_df['calculated_exec_speed'] = fuzzer_df['execs_done'] / fuzzer_df['runtime']
    fuzzer_df.drop(columns=['start_time', 'last_update'], inplace=True)
    return fuzzer_df


def get_mean_fuzzing_stats(log_folder, experiment_name):
    log_dfs = []
    for i in range(0, 10): 
        file_path = os.path.join(log_folder, '{}_{}_filtered_fuzzer_stats'.format(experiment_name, i))
        log_dfs.append(get_fuzzer_data(file_path))

    dfs = [df.drop(df.columns[[0,1,2,7]], axis=1) for df in log_dfs]
    mean_df = sum(dfs)/len(dfs)
    result_df = pd.concat([log_dfs[0][['fuzzer', 'library', 'fuzz target']], mean_df], axis=1)
    return result_df


if __name__ == "__main__":
    # process initial corpus
    log_folder = './log/initial-corpus-final'
    experiment_name="initial-corpus-final"
    file_path = os.path.join(log_folder, '{}_{}_filtered_fuzzer_stats'.format(experiment_name, 0))
    get_fuzzer_data(file_path).to_csv('{}/fuzzing_stats_initial_seeds.csv'.format(log_folder), index=False)
    
# log_folder = '../log'
# experiment_name1 = 'afl-aflpp-libfuzzer-initial-experiments'
# experiment_name2 = 'aflgo-initial-experiments'
# experiment_name3 = 'ffd-fixed-experiments'

# experiment_name = 'aflpp-24h-corpus1'
# file_path = os.path.join(log_folder, '{}_{}_filtered_fuzzer_stats'.format(experiment_name, 0))
# get_fuzzer_data(file_path).to_csv('fuzzing_stats_initial_seeds.csv', index=False)

# result_dfs = [get_mean_fuzzing_stats(log_folder, experiment_name1), get_mean_fuzzing_stats(log_folder, experiment_name2), get_mean_fuzzing_stats(log_folder, experiment_name3)]
# concatenated_result = pd.concat(result_dfs)
# concatenated_result.to_csv('fuzzing_stats_experiments.csv', index=False)
