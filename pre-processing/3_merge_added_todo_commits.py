import os

added_todo_files = os.listdir('./added_todo_commits/')
with open('./added_todo_commits.out', 'w') as fout:
    for f in added_todo_files:
        with open('./added_todo_commits/' + f, 'r') as fin:
            if os.stat('./added_todo_commits/' + f).st_size == 0:
                continue
            else:
                for line in fin:
                    fout.write(line)
