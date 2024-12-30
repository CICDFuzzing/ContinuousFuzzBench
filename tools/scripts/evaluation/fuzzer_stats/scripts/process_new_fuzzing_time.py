import glob
import os
import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu, rankdata


def mann_whitney_u_test(sample1, sample2, alternative):
    U1, p = mannwhitneyu(sample1, sample2, alternative=alternative, method='auto')
    return p



# Define the base pattern to search
home_dir = os.path.expanduser("~")

rows = ['libpng_4_1', 'libsndfile_2_1', 'libsndfile_7_1', 'libsndfile_15_1', 'libtiff_6_1', 'libtiff_7_1', 'libtiff_9_1', 'libtiff_10_1', 'libxml2_1_2', 'libxml2_2_1', 'libxml2_8_1', 'libxml2_10_2', 'libxml2_12_2', 'libxml2_14_1', 'libxml2_15_1', 'libxml2_16_1', 'libxml2_16_2', 'openssl_1_3', 'openssl_1_5', 'openssl_4_4', 'openssl_5_1', 'openssl_6_4', 'openssl_6_5', 'openssl_6_6', 'openssl_7_2', 'openssl_7_4', 'openssl_8_1', 'openssl_9_1', 'openssl_10_5', 'openssl_11_4', 'openssl_11_6', 'openssl_12_6', 'openssl_13_2', 'openssl_16_6', 'openssl_17_2', 'openssl_17_4', 'openssl_18_5', 'openssl_19_1', 'openssl_20_3', 'openssl_20_4', 'php_4_1', 'php_6_2', 'php_11_2', 'php_15_2', 'php_16_3', 'poppler_3_1', 'poppler_9_1', 'poppler_17_1', 'sqlite3_18_1', 'sqlite3_20_1']
columns = ['afl', 'aflpp', 'aflgo', 'aflgoe', 'ffd']
result_df = pd.DataFrame([[[None] * 10 for _ in range(len(columns))] for _ in range(len(rows))], index=rows, columns=columns)

log_path = 'research/thesis/scratch-dir/log-data'
pattern = '*/ar/*/*/*/*/findings/plot_data'

for fuzzer_name in ['afl', 'aflgo', 'aflgoe', 'ffd']:
    pattern_path = os.path.join(home_dir, log_path, fuzzer_name, pattern)
    for file_path in glob.glob(pattern_path, recursive=True):
        file_name = os.path.basename(file_path)
        #print(f'Processing: {file_path}')
        df = pd.read_csv(file_path, 
                        names=['#_unix_time', 'cycles_done', 'cur_path', 'paths_total', 'pending_total', 'pending_favs', 'map_size', 'unique_crashes', 'unique_hangs', 'max_depth', 'execs_per_sec'], 
                        header=None, skiprows=1)
        fuzzer = file_path.split('/')[7]
        benchmark = file_path.split('/')[-5]
        iter_num = int(file_path.split('/')[-3])

        if len(df) > 0:
            fuzzing_time = df['#_unix_time'].iloc[len(df)-1] - df['#_unix_time'].iloc[0]
            result_df.at[benchmark, fuzzer][iter_num] = fuzzing_time
        else:
            result_df.at[benchmark, fuzzer][iter_num] = 0


# workaround for aflpp
aflpp_pattern = '*/ar/*/*/*/*/findings/default/plot_data'
aflpp_pattern_path = os.path.join(home_dir, log_path, 'aflpp', aflpp_pattern)
for file_path in glob.glob(aflpp_pattern_path, recursive=True):
    file_name = os.path.basename(file_path)
    print(f'Processing: {file_path}')
    df = pd.read_csv(file_path, 
                    names=['#_relative_time', 'cycles_done', 'cur_path', 'paths_total', 'pending_total', 'pending_favs', 'map_size', 'unique_crashes', 'unique_hangs', 'max_depth', 'execs_per_sec', 'total_execs', 'edges_found'], 
                    header=None, skiprows=1)
    fuzzer = 'aflpp'
    benchmark = file_path.split('/')[-6]
    iter_num = int(file_path.split('/')[-4])

    if len(df) > 0:
        fuzzing_time = df['#_relative_time'].iloc[len(df)-1]
        result_df.at[benchmark, fuzzer][iter_num] = fuzzing_time
    else:
        result_df.at[benchmark, fuzzer][iter_num] = 0

for row_idx, row in result_df.iterrows():
    for col_idx, cell in row.items():
        if None in cell:
            print(f"None found at row {row_idx}, column '{col_idx}'")

mean_df = result_df.applymap(lambda x: np.mean(x))
print(mean_df)

# store result_df

# formatting
for benchmark_name in rows:
    mean_results = mean_df.loc[benchmark_name].values
    full_results = result_df.loc[benchmark_name].values
    max_value = np.max(mean_results)
    indices_of_max = np.where(mean_results == max_value)[0]
    if len(indices_of_max) == 1:
        index_of_max = indices_of_max[0]
        # perform stats tests
        rank = 0
        for i in range(len(mean_results)):
            if i != index_of_max:
                # print('max')
                # print(full_results[index_of_max])
                # print('others')
                # print(full_results[i])
                p = mann_whitney_u_test(full_results[index_of_max], full_results[i], 'greater')
                # print('p value:')
                # print(p)
                if p < 0.05:
                    rank += 1
        if rank == 4:
            max_result = r'\textbf{' + f"{mean_results[index_of_max]:.0f}" + '}'
            max_result = r'\colorbox{gray!40}{' + max_result + '}'
        else:
            max_result = r'\textbf{' + f"{mean_results[index_of_max]:.0f}" + '}'
        formatted_results = [f"{x:.0f}" if isinstance(x, float) else str(x) for x in mean_results]
        formatted_results[index_of_max] = max_result
        formatted = ' & '.join(formatted_results)
        benchmark_name = benchmark_name.replace('_', r'\_')
        print(f'{benchmark_name} & {formatted} \\\\')
    else:
        formatted_results = [f"{x:.0f}" if isinstance(x, float) else str(x) for x in mean_results]
        if len(indices_of_max) < 5:
            for index_of_max in indices_of_max:
                formatted_results[index_of_max] = r'\textbf{' + f"{mean_results[index_of_max]:.0f}" + '}'
        formatted = ' & '.join(formatted_results)
        benchmark_name = benchmark_name.replace('_', r'\_')
        print(f'{benchmark_name} & {formatted} \\\\')


# lib_df = pd.read_csv('/home/mhuang/research/thesis/ContinuousFuzzBench/tools/scripts/evaluation/fuzzer_stats/log/libfuzzer_fuzzer_stats')
# # formatting
# for benchmark_name in rows:
#     mean_results = mean_df.loc[benchmark_name].values
#     formatted_results = [f"{x:.0f}" if isinstance(x, float) else str(x) for x in mean_results]
#     formatted = ' & '.join(formatted_results)
#     libfuzzer_stats = lib_df.loc[lib_df['TARGET'] == benchmark_name, 'runtime'].iloc[0]
#     benchmark_name = benchmark_name.replace('_', r'\_')
#     print(f'{benchmark_name} & {formatted} & {libfuzzer_stats:.0f} \\\\')

