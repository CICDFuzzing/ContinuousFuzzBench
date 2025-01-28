import os
import random
import pandas as pd
import subprocess


# >>> lst=[11, 7.10526, 11, 10.3889, 11.9048, 13.2941, 8.13043, 7.95238]
# >>> sum(lst)/len(lst)
# 10.096983750000001

def select_random_commits(commit_dir, tmp_dir, lib_versions):
    for file_name in os.listdir(commit_dir):
        # Check if CSV file
        if file_name.endswith('.csv'):
            lib_name = file_name.split('_')[0]
            lib_url = lib_versions[lib_name]
            # Construct the full file path
            file_path = os.path.join(commit_dir, file_name)
            df = pd.read_csv(file_path)
            # Delete the last row
            df = df.drop(df.index[-1])
            num_of_targets = 0
            unchecked_ids = list(range(0, len(df)))
            while(num_of_targets < 10 or num_of_targets >100):
                commit_id = random.choice(unchecked_ids)
                unchecked_ids.remove(commit_id)
                commit_hash = df.at[commit_id, 'Commit_Hash']
                # run the terminal command
                try:
                    result = subprocess.run(
                        ["./process_commits.sh", lib_name, lib_url, commit_hash, tmp_dir],
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    if result.returncode == 0:
                        result_output = result.stdout
                        result_output = result_output.replace('\n', '')
                        num_of_targets = int(result_output)
                        print('Number of targets: {}'.format(num_of_targets))
                    else:
                        print('Execution error: {}'.format(result.stderr))
                except FileNotFoundError:
                    print('The shell script cannot be found.')
                except Exception as e:
                    print('Error: {}'.format(e))

            assert num_of_targets >= 10 and num_of_targets <= 100
            print(f'Library: {lib_name}, commit hash: {commit_hash}, number of new targets: {num_of_targets}')
            


if __name__ == "__main__":
    lib_dict = {
        'libpng': 'https://github.com/glennrp/libpng.git',
        'libsndfile': 'https://github.com/libsndfile/libsndfile.git',
        'libtiff': 'https://gitlab.com/libtiff/libtiff.git',
        'libxml2': 'https://gitlab.gnome.org/GNOME/libxml2.git',
        'openssl': 'https://github.com/openssl/openssl.git',
        'php-src': 'https://github.com/php/php-src.git',
        'poppler': 'https://gitlab.freedesktop.org/poppler/poppler.git'
    }
    select_random_commits('commits_for_full_experiments', '/home/mhuang/research/thesis/ContinuousFuzzBench/tools/scripts/sensitivity/utility/tmp', lib_dict)

