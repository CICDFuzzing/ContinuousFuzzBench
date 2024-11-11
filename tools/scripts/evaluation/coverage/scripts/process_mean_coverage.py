import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


def format_target_function(file_path, custom_order):
    df = pd.read_csv(file_path, names=['function', 'benchmark'], header=None)
    df['benchmark'] = df['benchmark'].str.extract(r'aflgo_([^_]+_[^_]+_[^_]+)_build\.log')
    df['benchmark'] = pd.Categorical(df['benchmark'], categories=custom_order, ordered=True)
    df = df.sort_values('benchmark').reset_index(drop=True)
    cols = df.columns.tolist()
    df = df[[cols[1], cols[0]]]
    formatted_rows = df.apply(
        lambda row: ' & '.join(
            f"{x:.2f}".replace('_', r'\_') if isinstance(x, (int, float)) else str(x).replace('_', r'\_') for x in row
        ) + ' \\\\',
        axis=1
    )

    # Print each formatted row
    for row in formatted_rows:
        print(row)
    return df


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


def format_target_function_coverage(file_name, custom_order):
    df = pd.read_csv(file_name)
    df['TARGET'] = pd.Categorical(df['TARGET'], categories=custom_order, ordered=True)
    df = df.sort_values('TARGET').reset_index(drop=True)
    # Format each row as "x & x & x & x & x \\"
    df = df[['TARGET', 'Lines', 'Cover.1', 'Branches', 'Cover.2']]
    #df = df[['TARGET', 'Functions', 'Executed', 'Lines', 'Cover.1', 'Branches', 'Cover.2']]
    df['TARGET'] = df['TARGET'].str.replace('_', r'\_')
    #df['Filename'] = df['Filename'].str.replace('_', r'\_')
    formatted_rows = df.apply(
        lambda row: ' & '.join(f"{x:.3f}" if isinstance(x, (int, float)) else str(x) for x in row) + ' \\\\', 
        axis=1
    )

    # Print each formatted row
    for row in formatted_rows:
        print(row)
    return df


def format_total_coverage(file_name, custom_order):
    df = pd.read_csv(file_name)
    df['TARGET'] = pd.Categorical(df['TARGET'], categories=custom_order, ordered=True)
    df = df.sort_values('TARGET').reset_index(drop=True)
    # Format each row as "x & x & x & x & x \\"
    df = df[['TARGET', 'Functions', 'Executed', 'Lines', 'Cover.1', 'Branches', 'Cover.2']]
    df['TARGET'] = df['TARGET'].str.replace('_', r'\_')
    formatted_rows = df.apply(
        lambda row: ' & '.join(f"{x:.3f}" if isinstance(x, (int, float)) else str(x) for x in row) + ' \\\\', 
        axis=1
    )

    # Print each formatted row
    for row in formatted_rows:
        print(row)
    return df


def format_total_coverage_branch_comparison_table(log_path, file_name, col_name, feature_name, custom_order):
    dfs = {}
    for fuzzer in ['afl', 'aflpp', 'libfuzzer', 'aflgo', 'ffd']:
        df = pd.read_csv(os.path.join(log_path, '{}_{}'.format(fuzzer, file_name)))
        if 'time' in df.columns:
            df['time'] = df['time'].str.replace('s', '', regex=False)
            df['time'] = pd.to_numeric(df['time'])
        df[col_name] = pd.Categorical(df[col_name], categories=custom_order, ordered=True)
        df = df.sort_values(col_name).reset_index(drop=True)
        dfs[fuzzer] = df
    cover_columns = [df[feature_name] for df in dfs.values()]
    combined_df = pd.concat(cover_columns, axis=1)
    combined_df.columns = [f'{fuzzer}' for fuzzer in dfs.keys()]

    combined_df[col_name] = dfs['afl'][col_name].reset_index(drop=True)
    cols = [col_name] + [col for col in combined_df.columns if col != col_name]
    combined_df = combined_df[cols]

    print(combined_df)

    # # Format each row as "x & x & x & x & x \\"
    formatted_combined_df = combined_df.copy()
    formatted_combined_df[col_name] = formatted_combined_df[col_name].str.replace('_', r'\_')
    formatted_rows = formatted_combined_df.apply(
        lambda row: ' & '.join(
            f"\\textbf{{{x:.0f}}}" if x == max(row[1:]) and isinstance(x, (int, float)) and not all(value == row[1] for value in row[1:]) else f"{x:.0f}" 
            if isinstance(x, (int, float)) else str(x) 
            for x in row
        ) + ' \\\\', 
        axis=1
    ).tolist()

    # Print each row fully expanded without the index
    for row in formatted_rows:
        print(row)
    return combined_df


def process_bug_analysis_results(log_path, file_name, col_name, custom_order):
    dfs = {}
    for fuzzer in ['afl', 'aflpp', 'libfuzzer', 'aflgo', 'aflgoexp', 'ffd']:
        df = pd.read_csv(os.path.join(log_path, '{}_{}'.format(fuzzer, file_name)))
        df[col_name] = pd.Categorical(df[col_name], categories=custom_order, ordered=True)
        df = df.sort_values(col_name).reset_index(drop=True)
        dfs[fuzzer] = df
    print(dfs)

    results = []
    for target in custom_order:
        for fuzzer, df in dfs.items():
            row = df[df['target'] == target]
            if not row.empty:
                feature_r_name = 'R_{}'.format(fuzzer)
                feature_t_name = 'T_{}'.format(fuzzer)
                results.append({
                'target': target,
                feature_r_name: row['survival_time_reached'].values[0],
                feature_t_name: row['survival_time_triggered'].values[0]
            })
    
    combined_df = pd.DataFrame(results)
    combined_df = combined_df.groupby('target').agg(lambda x: x.dropna().iloc[0] if x.notna().any() else np.nan).reset_index()
    combined_df_trimmed = combined_df.dropna(how='all')
    print(combined_df)
    print(combined_df_trimmed.columns)

    combined_df_trimmed = combined_df_trimmed[['target', 'R_afl', 'T_afl', 'R_aflpp', 'T_aflpp', 'R_libfuzzer', 'T_libfuzzer', 'R_aflgo', 'T_aflgo',
       'R_aflgoexp', 'T_aflgoexp', 'R_ffd', 'T_ffd']]
    print(combined_df_trimmed)

    combined_df_trimmed[col_name] = combined_df_trimmed[col_name].str.replace('_', r'\_')
    formatted_rows = combined_df_trimmed.apply(
        lambda row: ' & '.join(
            "" if pd.isna(x) else (
                f"\\textbf{{{x:.0f}}}" if x == min(row[1:]) and isinstance(x, (int, float)) and not all(value == row[1] for value in row[1:])
                else f"{x:.0f}" if isinstance(x, (int, float))
                else str(x)
            )
            for x in row
        ) + ' \\\\', 
        axis=1
    ).tolist()

    # Print each row fully expanded without the index
    for row in formatted_rows:
        print(row)



if __name__ == "__main__":

    custom_order = ['libpng_4_1', 'libsndfile_2_1', 'libsndfile_7_1', 'libsndfile_15_1', 'libtiff_6_1', 'libtiff_7_1', 'libtiff_9_1', 'libtiff_10_1', 'libxml2_1_2', 'libxml2_2_1', 'libxml2_8_1', 'libxml2_10_2', 'libxml2_12_2', 'libxml2_14_1', 'libxml2_15_1', 'libxml2_16_1', 'libxml2_16_2', 'openssl_1_3', 'openssl_1_5', 'openssl_4_4', 'openssl_5_1', 'openssl_6_4', 'openssl_6_5', 'openssl_6_6', 'openssl_7_2', 'openssl_7_4', 'openssl_8_1', 'openssl_9_1', 'openssl_10_5', 'openssl_11_4', 'openssl_11_6', 'openssl_12_6', 'openssl_13_2', 'openssl_16_6', 'openssl_17_2', 'openssl_17_4', 'openssl_18_5', 'openssl_19_1', 'openssl_20_3', 'openssl_20_4', 'php_4_1', 'php_6_2', 'php_11_2', 'php_15_2', 'php_16_3', 'poppler_3_1', 'poppler_9_1', 'poppler_17_1', 'sqlite3_18_1', 'sqlite3_20_1']

    # target_function_path = 'target_functions.csv'
    # format_target_function(target_function_path, custom_order)

    #for fuzzer in ['aflgoexp']:
    # for fuzzer in ['afl', 'aflpp', 'libfuzzer', 'aflgo', 'aflgoexp', 'ffd']:
    #     print(fuzzer)
        #process_mean_total_coverage("/home/huicongh/ContinuousFuzzBench/tools/scripts/evaluation/log/total_coverage/{}".format(fuzzer), "../log/mean_coverage/mean_total_coverage/{}_mean_total_coverage".format(fuzzer))
        #process_mean_target_function_coverage("/home/huicongh/ContinuousFuzzBench/tools/scripts/evaluation/log/target_function_coverage/{}".format(fuzzer), "../log/mean_coverage/mean_target_function_coverage/{}_mean_target_function_coverage".format(fuzzer))
        #format_total_coverage('../log/mean_coverage/mean_total_coverage/{}_mean_total_coverage'.format(fuzzer), custom_order)
        #format_target_function_coverage('../log/mean_coverage/mean_target_function_coverage/{}_mean_target_function_coverage'.format(fuzzer), custom_order)
 
    #format_total_coverage_branch_comparison_table('/home/huicongh/ContinuousFuzzBench/tools/scripts/evaluation/fuzzer_stats/log', 'fuzzer_stats', 'TARGET', 'runtime', custom_order)
    df = format_total_coverage_branch_comparison_table('/home/huicongh/ContinuousFuzzBench/tools/scripts/evaluation/build_time/log', 'build_time', 'benchmark', 'time', custom_order)
    #process_bug_analysis_results('/home/huicongh/ContinuousFuzzBench/tools/scripts/evaluation/bug_analysis/log', 'survival_analysis', 'target', custom_order)

    x = df['benchmark']
    y_values = df.set_index('benchmark')  

    # Plotting
    fig, ax = plt.subplots(figsize=(24,30))
    y_values.plot(kind='bar', stacked=True, ax=ax, cmap='viridis')

    # Adding labels and title
    ax.set_xlabel('Benchmark', fontsize=26)
    ax.set_ylabel('Time (s)', fontsize=26)
    ax.set_title('Instrumentation Time for each Benchmark', fontsize=26)
    plt.xticks(rotation=90) 
    plt.xticks(fontsize=26)
    plt.yticks(fontsize=26)
    ax.legend(fontsize=26)
    plt.savefig('instrumentation_time_complete_large.png', format="png", dpi=300)


    x_values = ['afl', 'aflpp', 'libfuzzer', 'aflgo', 'ffd']
    y_values = [6.4, 35, 2.2, 228.3, 21.2]

    # Create a bar chart
    plt.figure(figsize=(8, 6))  
    plt.bar(x_values, y_values) 

    plt.xlabel('Fuzzers', fontsize=12)
    plt.ylabel('Time (s)', fontsize=12)
    plt.title('Build Time for each Fuzzer', fontsize=12)
    plt.savefig('build_time_complete.png', format="png", dpi=300)

