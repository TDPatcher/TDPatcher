import pickle

base_dir = '/data1/icse-todo-reminder/data_split/'

with open(base_dir + 'anchor_samples_dict.pkl', 'rb') as handler:
    anchor_samples = pickle.load(handler)

with open(base_dir + 'positive_samples_dict.pkl', 'rb') as handler:
    positive_samples = pickle.load(handler)

with open(base_dir + 'negative_samples_dict.pkl', 'rb') as handler:
    negative_samples = pickle.load(handler)

with open('./anchor_samples', 'w') as fa, \
    open('./positive_samples', 'w') as fp, \
    open('./negative_samples', 'w') as fn:

    # for k, v in anchor_samples.items():
    for i in range(len(anchor_samples)):
        # print(k)
        # print(v)
        print(i)
        if i in anchor_samples:
            anchor_todo_comment_statement = anchor_samples[i]['anchor_todo_comment_statement']
            anchor_todo_context = anchor_samples[i]['anchor_todo_context']
            fa.write(anchor_todo_comment_statement + '\t' + anchor_todo_context)
            fa.write('\n')

            positive_todo_comment_statement = positive_samples[i]['positive_todo_comment_statement']
            positive_todo_context = positive_samples[i]['positive_todo_context']
            fp.write(positive_todo_comment_statement + '\t' + positive_todo_context)
            fp.write('\n')

            negative_todo_comment_statement = negative_samples[i]['negative_todo_comment_statement']
            negative_todo_context = negative_samples[i]['negative_todo_context']
            fn.write(negative_todo_comment_statement + '\t' + negative_todo_context)
            fn.write('\n')

print("Finished!")


