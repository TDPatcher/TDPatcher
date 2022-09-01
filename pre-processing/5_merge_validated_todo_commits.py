import os

added_todo_files = os.listdir('./added_todo_commits_validate/')
with open('./added_todo_commits.validate', 'w') as fout:
    for f in added_todo_files:
        with open('./added_todo_commits_validate/' + f, 'r') as fin:
            if os.stat('./added_todo_commits_validate/' + f).st_size == 0:
                continue
            else:
                for line in fin:
                    fout.write(line)
