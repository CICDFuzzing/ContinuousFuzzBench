from scipy.stats import mannwhitneyu, rankdata
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import json
import os


def mann_whitney_u_test(sample1, sample2, alternative):
    U1, p = mannwhitneyu(sample1, sample2, alternative=alternative, method='auto')
    return p


def effective_size(sample1, sample2):
    # Effective size: A12
    m = len(sample1)
    n = len(sample2)
    rank_results = rankdata(sample1 + sample2)
    r1 = sum(rank_results[0:m])
    # A = (r1/m - (m+1)/2)/n # formula (14) in Vargha and Delaney, 2000
    A_12 = (2 * r1 - m * (m + 1)) / (2 * n * m)
    return A_12


def get_time_to_bug(file_path, results, fuzzer_name=None) -> dict:
    with open(file_path, 'r') as file:
        data = json.load(file).get('results', {})
    for fuzzer, f_data in data.items():
        for target, t_data in f_data.items():
            for program, p_data in t_data.items():
                for run, r_data in p_data.items():
                    for metric, m_data in r_data.items():
                        #for bug, time in m_data.items():
                        if fuzzer_name:
                            results[fuzzer_name][metric][int(run)] += len(m_data)
                        else:
                            results[fuzzer][metric][int(run)] += len(m_data)
    return results


def get_p_val_for_num_bug(result_dict: dict, fuzzers, metric, alternative):
    p_matrix = [[np.nan for _ in range(6)] for _ in range(6)]
    for i in range(len(fuzzers)):
        for j in range(len(fuzzers)):
            if j <= i:
                pass
            else:
                print('{}, {}'.format(fuzzers[i], fuzzers[j]))
                p = mann_whitney_u_test(result_dict[fuzzers[i]][metric], result_dict[fuzzers[j]][metric], alternative)
                print(p)
                p_matrix[i][j] = p
                if alternative == 'two-sided':
                    p_matrix[j][i] = p
    for row in p_matrix:
        print(row)
    return p_matrix


def p_val_heatmap_for_num_bug(matrix, fig_title, file_name):
    # Create the heatmap
    plt.figure(figsize=(10, 8))  
    # cbPalette = ['#CC79A7', '#D55E00', '#0072B2', '#F0E442', '#009E73', '#56B4E9', '#E69F00', '#999999']
    # cmap=sns.color_palette(cbPalette)
    mask = np.isnan(matrix)
    ax = sns.heatmap(matrix, cmap='viridis_r', mask=mask, annot=True, fmt=".6f")
    # Set custom axis labels
    ax.set_xticklabels(fuzzers)
    ax.set_yticklabels(fuzzers)
    plt.xticks(rotation=30)
    plt.yticks(rotation=30)
    # Customize and show the plot
    plt.title(fig_title, fontsize=20)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    # Save the plot locally
    # plt.gca().invert_yaxis()
    # plt.gca().invert_xaxis()
    plt.savefig(file_name, format="png", dpi=300)


def test_and_format_coverage(fuzzers, benchmarks, col_name, coverage_log_path):
    for benchmark in benchmarks:
        log_results = []
        for fuzzer in fuzzers:
            fuzzer_log_path = os.path.join(coverage_log_path, fuzzer)
            file_prefix = f'{fuzzer}_{benchmark}'
            for file_name in os.listdir(fuzzer_log_path):
                if file_name.startswith(file_prefix):
                    file_path = os.path.join(fuzzer_log_path, file_name)
                    if os.path.isfile(file_path):
                        try:
                            #print(f"Processing file: {file_name}")
                            df = pd.read_csv(file_path)
                            df[col_name] = df[col_name].fillna('0%')
                            df[col_name] = df[col_name].str.rstrip('%').astype(float)
                            #print(df[col_name].values) 
                            log_results.append(df[col_name].values)
                        except Exception as e:
                            print(f"Error processing {file_name}: {e}")

        # format benchmark name
        benchmark_name = benchmark.replace('_', r'\_')
        # get the index of the one with the max mean value
        mean_results = [result.mean() for result in log_results]
        max_value = np.max(mean_results)
        indices_of_max = np.where(mean_results == max_value)[0]
        if len(indices_of_max) == 1:
            index_of_max = indices_of_max[0]
            # perform stats tests
            rank = 0
            for i in range(len(log_results)):
                if i != index_of_max:
                    p = mann_whitney_u_test(log_results[index_of_max], log_results[i], 'greater')
                    if p < 0.05:
                        rank += 1
            if rank == 5:
                mean_results[index_of_max] = r'\textbf{' + f"{mean_results[index_of_max]:.3f}" + '}'
                mean_results[index_of_max] = r'\colorbox{gray!40}{' + mean_results[index_of_max] + '}'
                formatted_results = ' & '.join(f"{x:.3f}" if isinstance(x, float) else str(x) for x in mean_results)
                print(f'{benchmark_name} & {formatted_results} \\\\')
            else:
                mean_results[index_of_max] = r'\textbf{' + f"{mean_results[index_of_max]:.3f}" + '}'
                formatted_results = ' & '.join(f"{x:.3f}" if isinstance(x, float) else str(x) for x in mean_results)
                print(f'{benchmark_name} & {formatted_results} \\\\')
        else:
            if len(indices_of_max) < 6:
                for index_of_max in indices_of_max:
                    mean_results[index_of_max] = r'\textbf{' + f"{mean_results[index_of_max]:.3f}" + '}'
            formatted_results = ' & '.join(f"{x:.3f}" if isinstance(x, float) else str(x) for x in mean_results)
            print(f'{benchmark_name} & {formatted_results} \\\\')


def test_and_format_fuzzer_stats(fuzzers, benchmarks, col_name, coverage_log_path):
    for benchmark in benchmarks:
        log_results = []
        for fuzzer in fuzzers:
            fuzzer_log_path = os.path.join(coverage_log_path, fuzzer)
            file_prefix = f'{fuzzer}_{benchmark}'
            for file_name in os.listdir(fuzzer_log_path):
                if file_name.startswith(file_prefix):
                    file_path = os.path.join(fuzzer_log_path, file_name)
                    if os.path.isfile(file_path):
                        try:
                            #print(f"Processing file: {file_name}")
                            if fuzzer == 'libfuzzer':
                                df = pd.read_csv(file_path)
                            else:
                                df = pd.read_csv(file_path, names=['fuzzer', 'target', 'program', 'iter', 'start_time', 'last_update', 'execs_done', 'unique_crashes'], header=None)
                            if col_name == 'runtime' and fuzzer != 'libfuzzer':
                                df['runtime'] = df['last_update'] - df['start_time']
                            log_results.append(df[col_name].values)
                        except Exception as e:
                            print(f"Error processing {file_name}: {e}")
        # format benchmark name
        benchmark_name = benchmark.replace('_', r'\_')
        # get the index of the one with the max mean value
        mean_results = [result.mean() for result in log_results]
        max_value = np.max(mean_results)
        indices_of_max = np.where(mean_results == max_value)[0]
        if len(indices_of_max) == 1:
            index_of_max = indices_of_max[0]
            # perform stats tests
            rank = 0
            for i in range(len(log_results)):
                if i != index_of_max:
                    p = mann_whitney_u_test(log_results[index_of_max], log_results[i], 'greater')
                    if p < 0.05:
                        rank += 1
            if rank == 5:
                mean_results[index_of_max] = r'\textbf{' + f"{mean_results[index_of_max]:.0f}" + '}'
                mean_results[index_of_max] = r'\colorbox{gray!40}{' + mean_results[index_of_max] + '}'
                formatted_results = ' & '.join(f"{x:.0f}" if isinstance(x, float) else str(x) for x in mean_results)
                print(f'{benchmark_name} & {formatted_results} \\\\')
            else:
                mean_results[index_of_max] = r'\textbf{' + f"{mean_results[index_of_max]:.0f}" + '}'
                formatted_results = ' & '.join(f"{x:.0f}" if isinstance(x, float) else str(x) for x in mean_results)
                print(f'{benchmark_name} & {formatted_results} \\\\')
        else:
            if len(indices_of_max) < 6:
                for index_of_max in indices_of_max:
                    mean_results[index_of_max] = r'\textbf{' + f"{mean_results[index_of_max]:.0f}" + '}'
            formatted_results = ' & '.join(f"{x:.0f}" if isinstance(x, float) else str(x) for x in mean_results)
            print(f'{benchmark_name} & {formatted_results} \\\\')


if __name__ == "__main__":
    fuzzers = ['afl', 'aflplusplus', 'libfuzzer', 'aflgo', 'aflgoexp', 'ffd']

    # Get the number of bugs reached and triggered for all fuzzers
    # num_trial= 10
    # results = {
    #     'afl': {'reached': [0]*num_trial, 'triggered': [0]*num_trial},
    #     'aflplusplus': {'reached':[0]*num_trial, 'triggered': [0]*num_trial},
    #     'libfuzzer': {'reached': [0]*num_trial, 'triggered': [0]*num_trial},
    #     'aflgo': {'reached': [0]*num_trial, 'triggered': [0]*num_trial},
    #     'aflgoexp': {'reached': [0]*num_trial, 'triggered': [0]*num_trial},
    #     'ffd': {'reached': [0]*num_trial, 'triggered': [0]*num_trial}
    # }

    # file_paths = ['../bug_analysis/log/afl/afl-experiments-and-php-results.json', 
    #               '../bug_analysis/log/aflgo/aflgo-experiments-results.json', 
    #               '../bug_analysis/log/aflpp/aflpp-experiments-results.json',
    #               '../bug_analysis/log/aflpp/aflpp-php-results.json',
    #               '../bug_analysis/log/ffd/ffd-experiments-results.json',
    #               '../bug_analysis/log/libfuzzer/libfuzzer-experiments1-results.json',
    #               '../bug_analysis/log/libfuzzer/libfuzzer-experiments2-results.json',
    #               '../bug_analysis/log/libfuzzer/libfuzzer-experiments3-results.json',
    #               '../bug_analysis/log/libfuzzer/libfuzzer-experiments4-results.json']
    
    # aflgoexp_paths = ['../bug_analysis/log/aflgoexp/aflgo-exp-experiments-1-results.json',
    #                   '../bug_analysis/log/aflgoexp/aflgo-exp-experiments-2-results.json',
    #                   '../bug_analysis/log/aflgoexp/aflgo-exp-experiments-3-results.json']
    
    # for path in file_paths:
    #     get_time_to_bug(path, results)

    # for path in aflgoexp_paths:
    #     get_time_to_bug(path, results, 'aflgoexp')

    # print(results)

    # with open('num_of_bug_rt.json', 'w') as json_file:
    #     json.dump(results, json_file)


    # Read the results and plot the heatmap
    with open('num_of_bug_rt.json', 'r') as json_file:
        num_bug_results = json.load(json_file)
    print(num_bug_results) 

    p_matrix_reached = get_p_val_for_num_bug(num_bug_results, fuzzers, 'reached', 'greater')
    p_matrix_triggered = get_p_val_for_num_bug(num_bug_results, fuzzers, 'triggered', 'greater')
    p_val_heatmap_for_num_bug(p_matrix_reached, 'P Values for the Number of Bugs Reached', 'bug_r_greater.png')
    p_val_heatmap_for_num_bug(p_matrix_triggered, 'P Values for the Number of Bugs Triggered', 'bug_t_greater.png')


    # stats tests for coverage
    # fuzzers2 = ['afl', 'aflpp', 'libfuzzer', 'aflgo', 'aflgoexp', 'ffd']
    # benchmarks = ['libpng_4_1', 'libsndfile_2_1', 'libsndfile_7_1', 'libsndfile_15_1', 'libtiff_6_1', 'libtiff_7_1', 'libtiff_9_1', 'libtiff_10_1', 'libxml2_1_2', 'libxml2_2_1', 'libxml2_8_1', 'libxml2_10_2', 'libxml2_12_2', 'libxml2_14_1', 'libxml2_15_1', 'libxml2_16_1', 'libxml2_16_2', 'openssl_1_3', 'openssl_1_5', 'openssl_4_4', 'openssl_5_1', 'openssl_6_4', 'openssl_6_5', 'openssl_6_6', 'openssl_7_2', 'openssl_7_4', 'openssl_8_1', 'openssl_9_1', 'openssl_10_5', 'openssl_11_4', 'openssl_11_6', 'openssl_12_6', 'openssl_13_2', 'openssl_16_6', 'openssl_17_2', 'openssl_17_4', 'openssl_18_5', 'openssl_19_1', 'openssl_20_3', 'openssl_20_4', 'php_4_1', 'php_6_2', 'php_11_2', 'php_15_2', 'php_16_3', 'poppler_3_1', 'poppler_9_1', 'poppler_17_1', 'sqlite3_18_1', 'sqlite3_20_1']
    
    # test_and_format_coverage(fuzzers2, benchmarks, 'Cover.2', '../coverage/log/total_coverage')
    # test_and_format_coverage(fuzzers2, benchmarks, 'Cover.2', '../coverage/log/target_function_coverage')

    # test_and_format_fuzzer_stats(fuzzers, benchmarks, 'execs_done', '../fuzzer_stats/log')
