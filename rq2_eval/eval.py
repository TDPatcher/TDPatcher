import os
import numpy as np
import collections

def get_ranking_position(result_fpath):
    with open(result_fpath, 'r') as fin:
        lines = fin.readlines()
        todo_lineno = int(lines[0].strip())
        for i in range(1, len(lines)):
            sim_score, line_range = lines[i].strip().split('\t')
            start_line = int(line_range.split('_')[0])
            end_line = int(line_range.split('_')[1])
            # print(todo_lineno, start_line, end_line)
            if todo_lineno >= start_line and todo_lineno <= end_line: 
                return i
    return None

def hits_count(candidate_ranks, k):
    '''
    candidate_ranks:
    list of candidates' ranks; one rank per question;
    length is a number of questions
    rank is a number from q to len(candidates of the question)
    e.g. [2, 3] means that first candidate has the rank 2,
                           second candidate has the rank 3
    k: number of top-ranked elements (k in hits@k metric)
    result: return Hits@k value for current ranking 
    '''
    count = 0
    for rank in candidate_ranks:
        if rank <= k:
            count += 1
    return count/(len(candidate_ranks)+1e-8)

def dcg_score(candidate_ranks, k):
    '''
    candidate_ranks:
    list of candidates' ranks; one rank per question;
    length is a number of questions
    rank is a number from q to len(candidates of the question)
    e.g. [2, 3] means that first candidate has the rank 2,
                           second candidate has the rank 3
    k: number of top-ranked elements (k in hits@k metric)
    
    result: return DCG@k value for current ranking
    '''
    score = 0
    for rank in candidate_ranks:
        if rank <= k:
            score += 1/np.log2(1+rank)
    return score/(len(candidate_ranks)+1e-8)

def get_candidate_ranks():
    candidate_ranks = []
    introduced_todo_commits = os.listdir('./test_set_result')
    for todo_commit in introduced_todo_commits[:]: 
        result_fpath = './test_set_result/' + todo_commit + '/patch.result'  
        if not os.path.exists(result_fpath):
            continue 
        rank_position = get_ranking_position(result_fpath)
        if rank_position:
            candidate_ranks.append(rank_position)
    return candidate_ranks

candidate_ranks =  get_candidate_ranks()
precision_at_1 = hits_count(candidate_ranks, 1)
precision_at_2 = hits_count(candidate_ranks, 2)
precision_at_3 = hits_count(candidate_ranks, 3)
precision_at_4 = hits_count(candidate_ranks, 4)
precision_at_5 = hits_count(candidate_ranks, 5)
print("===============================")
print("length of candidate_ranks:", len(candidate_ranks))
print("P@1:", precision_at_1)
print("P@2:", precision_at_2)
print("P@3:", precision_at_3)
print("P@4:", precision_at_4)
print("P@5:", precision_at_5)

dcg_at_1 = dcg_score(candidate_ranks, 1)
dcg_at_2 = dcg_score(candidate_ranks, 2)
dcg_at_3 = dcg_score(candidate_ranks, 3)
dcg_at_4 = dcg_score(candidate_ranks, 4)
dcg_at_5 = dcg_score(candidate_ranks, 5)
print("===============================")
print("DCG@1:", dcg_at_1)
print("DCG@2:", dcg_at_2)
print("DCG@3:", dcg_at_3)
print("DCG@4:", dcg_at_4)
print("DCG@5:", dcg_at_5)



# counter = collections.Counter( candidate_ranks )
# print(counter)
# print(640.0 / len(candidate_ranks))
# print(760.0 / len(candidate_ranks))
