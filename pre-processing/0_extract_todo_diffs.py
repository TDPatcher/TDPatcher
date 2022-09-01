import os
import json

# base_dir = "/data/zpgao/Github_Data/GitHub_Repo/python_repos_diff/"
# base_dir = "../python_repos_diff/"

def load_diff_dict( fname ):
    '''
    diff_dict: {}
    key: commit_id
    value: 
    {
        'commit_now':
        'commit_parent':
        'commit_diff':
        'commit_diff_pro':
        'commit_msg':
    }
    '''
    base_dir = "../../Github/python_repos_diff/"
    repo_id = fname.strip().strip('.json')
    with open(base_dir + fname, 'r') as diff_file:
        diff_dict = json.load(diff_file)
    return diff_dict 

def extract_todo_diff( fname, td_keywords ):
    '''
    todo_diff: {}
    key: commit_id
    value:
    {
        'repo_file':
        'commit_now':
        'commit_parent':
        'commit_diff':
        'commit_diff_pro':
        'commit_msg':
    }
    '''
    todo_diff = {}
    diff_dict = load_diff_dict( fname )

    for k, v in diff_dict.items():
        commit_diff = v['commit_diff'].lower()
        if any(word in commit_diff for word in td_keywords):
            key = k
            value = {}
            value['repo_file'] = fname
            value['commit_diff'] = v['commit_diff'] 
            value['commit_now'] = v['commit_now'] 
            value['commit_parent'] = v['commit_parent']
            value['commit_diff_pro'] = v['commit_diff_pro']
            value['commit_msg'] = v['commit_msg'] 
            todo_diff[key] = value 
    return todo_diff

td_keywords = [\
               'todo',  \
               'to do ', \
              ]

diff_files = os.listdir("../../Github/python_repos_diff/")
for fname in diff_files:
    if not fname.endswith('.json'):
        continue

    repo_id = fname.strip().strip('.json')
    print(fname, repo_id)

    todo_diff = extract_todo_diff(fname, td_keywords)
    # save todo_diff 
    # if todo_diff is not null
    if len(todo_diff) > 0:
        tgt_fpath = './todo_diff/' + str(repo_id) + '_todo.json'
        with open(tgt_fpath, 'w') as fp: 
            json.dump(todo_diff, fp)
    # break


