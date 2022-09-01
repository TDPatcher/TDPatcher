import os
import collections

def extract_TODO_comment( fpath ): 
    '''
    get all added TODO comments for a repo 
    '''
    added_TODO_comments = []
    with open(fpath, 'r') as f: 
        # each line is a commit 
        for commit in f:
            lines = commit.strip().split('<nl>')
            for line in lines:
                line = line.strip().lower()
                if line.startswith('+') and "todo" in line:
                    added_TODO_comments.append(line.lower())

    todo_comments_freq = dict(collections.Counter(added_TODO_comments))
    return todo_comments_freq

base_dir = './added_todo_commits/'
added_todo_files = os.listdir(base_dir)

for f in added_todo_files: 
    fpath = base_dir + f 
    print(f)
    # print(todo_comments_freq)
    # for k, v in todo_comments_freq.items():
    #     print(k, v)

    with open(fpath, 'r') as fin, \
        open('./added_todo_commits_validate/' + f, 'w') as fout:
        
        # todo_comments_freq = extract_TODO_comment( fpath ) 
        # print(todo_comments_freq)

        # if not todo_comments_freq: 
        #     continue 

        # for each commit in added_todo_commits
        for commit in fin:
            lines = commit.strip().split('<nl>')
            for line in lines:
                line = line.strip().lower()
                if line.startswith('+') and 'todo' in line:
                    todo_comment = line.lower()
                    fout.write(commit) 
                    break
                    # if todo_comments_freq[todo_comment] > 1:
                    # fout.write(commit)

    # break


