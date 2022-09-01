import os

base_dir = './todo_commits/' 
commits_files = os.listdir(base_dir)

for commit_file in commits_files:
    print(commit_file)
    with open(base_dir + commit_file, 'r') as fin, \
        open('./added_todo_commits/' + commit_file, 'w') as fout:

        for commit in fin:    
            # print(commit.strip())
            added_todo_count = 0
            commit_lines = commit.split('<nl>')
            for line in commit_lines:
                line = line.strip()
                if line.startswith('+') and "todo" in line.lower():
                    if '#' in line or "'" in line or '"' in line:
                        added_todo_count += 1
                        # print(line)

            if added_todo_count >= 1:
            # if added_todo_count >= 2:
                fout.write(commit)
             
        # break
    # break
