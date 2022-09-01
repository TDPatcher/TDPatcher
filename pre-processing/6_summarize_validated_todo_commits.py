import pickle

validate_commits2repo = {}
with open('./added_todo_commits.out', 'r') as fin:
    for line in fin:
        # print(line)
        repo_file, commit_now, commit_parent, \
        commit_msg_pro, commit_diff_pro, target_url = line.strip().split('\t')
        key = commit_now 
        value = {}
        value['repo_file'] = repo_file
        value['target_url'] = target_url 
        validate_commits2repo[key] = value
        # break

print("validate commits2repo:", len(validate_commits2repo))


with open('validate_commits2repo.pickle', 'wb') as handler:
    pickle.dump(validate_commits2repo, handler, protocol=pickle.HIGHEST_PROTOCOL)

with open('validate_commits2repo.out', 'w') as fout:
    for k, v in validate_commits2repo.items():
        commit_now = k
        repo_id = v['repo_file']
        target_url = v['target_url']
        fout.write(commit_now + '\t' + repo_id + '\t' + target_url)
        fout.write('\n')


validate_repo2commits = {}
for k, v in validate_commits2repo.items():
    commit = k
    repo_id = v['repo_file']
    if repo_id not in validate_repo2commits: 
        validate_repo2commits[repo_id] = [commit]  
    else:
        validate_repo2commits[repo_id].append(commit)

print("validate repo2commits:", len(validate_repo2commits))
with open('validate_repo2commits.pickle', 'wb') as handler:
    pickle.dump(validate_repo2commits, handler, protocol=pickle.HIGHEST_PROTOCOL)


