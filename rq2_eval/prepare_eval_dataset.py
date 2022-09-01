import os

def get_test_result(test_fpath):
    test_result = []
    with open(test_fpath, 'r') as fin:
        test_flines = fin.readlines()
        # print(test_flines)
        label = int(test_flines[0].strip())
        anchor_function = test_flines[1]
        # todo_lineno = anchor_function.strip().split('\t')[1]
        todo_comment = anchor_function.strip().split('\t')[2]
        candidate_function = test_flines[2]
        todo_lineno = candidate_function.strip().split('\t')[1]
        # todo_comment = candidate_function.strip().split('\t')[2]
        candidate_blocks = test_flines[3:]
        for test_block in candidate_blocks: 
            similarity_score = float(test_block.strip().split('\t')[-1])
            line_range = test_block.strip().split('\t')[0]
            test_result.append( (similarity_score, line_range, todo_lineno, todo_comment))
        ranked_test_result = sorted(test_result,key=lambda x: x[0], reverse=True)
    return ranked_test_result, todo_lineno  

introduced_todo_commits = os.listdir('./test_set_result')

for todo_commit in introduced_todo_commits: 
    files = os.listdir('./test_set_result/' + todo_commit )
    for f in files:
        if f.endswith('test.1'):
            todo_function = f

    todo_fpath = './test_set_result/' + todo_commit + '/' + todo_function 

    with open(todo_fpath, 'r') as fin:
        test_flines = fin.readlines()
        if len(test_flines) <= 1:
            continue 

    print(todo_fpath)
    ranked_test_result, todo_lineno =  get_test_result(todo_fpath)
    # print(ranked_test_result)
    # print(todo_lineno)
    with open('./test_set_result/' + todo_commit + '/patch.result', 'w') as fout:
        fout.write(str(todo_lineno) + '\n')
        for e in ranked_test_result:
            sim_score = e[0]
            line_range = e[1]
            fout.write(str(sim_score) + '\t' + str(line_range) + '\n')
    # print(todo_commit)
    # break

