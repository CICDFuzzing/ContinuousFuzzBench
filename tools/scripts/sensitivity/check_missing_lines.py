import bisect
import subprocess
import os


def check_missing_lines(target_file_path, repos_dir):
    line_numbers = {}
    total_lines = 0
    with open(target_file_path, 'r') as file:
        for line in file:
            # split the line into file name and line number
            file_name, line_number = line.strip().split(":")
            line_number = int(line_number)
            # update the line numbers
            if file_name in line_numbers:
                line_numbers[file_name].append(line_number)
            else:
                line_numbers[file_name] = [line_number]
            total_lines += 1
    
    total_num_of_missing_lines = 0
    for file_name, line_nums in line_numbers.items():
        print(f"{file_name}: {line_nums}")
        # cat [file_name] | wc =l -> return the num
        try:
            file_path = os.path.join(repos_dir, file_name)
            command = 'cat {} | wc -l'.format(file_path)
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                result_output = result.stdout.replace('\n', '')
                upper_limit = int(result_output)
                print(f'Execution output: {upper_limit}')
            else:
                print(f'Execution error: {result.stderr}')
        except Exception as e:
            print(f'Error: {e}')

        # check how many items in bounds are missed
        index_of_line = bisect.bisect_right(line_nums, upper_limit)
        num_of_missing_lines = len(line_nums) - index_of_line
        print(f'Number of missing lines: {num_of_missing_lines}')

        total_num_of_missing_lines += num_of_missing_lines

    missing_percent = (total_num_of_missing_lines/total_lines) * 100
    if missing_percent > 10:
        print(f'Need re-generation! Total number of missing lines: {total_num_of_missing_lines}, {missing_percent}% \n')
    else:
        print(f'Total number of missing lines: {total_num_of_missing_lines}, {missing_percent}% \n')

    
if __name__ == "__main__":
    cur_dir = os.getcwd()
    repo_archive_dir = 'utility/tmp/repo'
    repo_archive_dir = os.path.join(cur_dir, repo_archive_dir)

    commit_dir = 'utility/tmp/targets'
    commit_dir = os.path.join(cur_dir, commit_dir)

    # generalize to all files in the dir
    for file_name in os.listdir(commit_dir):
        target_file_path = os.path.join(commit_dir, file_name)
        repo_name = file_name.split('_')[0]
        repo_dir = os.path.join(repo_archive_dir, repo_name)
        print(file_name)
        check_missing_lines(target_file_path, repo_dir)

