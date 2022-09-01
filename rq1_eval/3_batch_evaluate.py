from sentence_transformers import SentenceTransformer, SentencesDataset, LoggingHandler, losses, InputExample
from sentence_transformers import models, util, datasets, evaluation, losses
import logging
import os
import gzip
import math
import pickle
from torch.utils.data import DataLoader
from datetime import datetime
from numpy import dot
from numpy.linalg import norm
from scipy.spatial import distance

def load_samples(fpath):
    samples = []
    with open(fpath, 'r') as f:
        for line in f:
            samples.append(line.strip())
    return samples

def evaluate_candidate_block(model, candidate_block):
    block_info = candidate_block.strip().split('\t') 
    # assert len(block_info) == 5 
    if len(block_info) == 5:
        candidate_line_range = block_info[0]
        anchor_statement = block_info[1] 
        anchor_context = block_info[2] 
        candidate_statement = block_info[3]
        candidate_context = block_info[4]
        
        anchor_input = anchor_statement + ' [SEP] ' + anchor_context
        anchor_vector = model.encode(anchor_input) 
        candidate_input = candidate_statement + ' [SEP] ' + candidate_context
        candidate_vector = model.encode(candidate_input) 
        similarity_score = 1 - distance.cosine(anchor_vector, candidate_vector)
        return similarity_score
    else:
        return -1

def prepare_candidate_inputs(candidate_blocks):
    candidate_inputs = []
    for candidate_block in candidate_blocks: 
        block_info = candidate_block.strip().split('\t') 
        candidate_statement = block_info[3]
        candidate_context = block_info[4]
        candidate_input = candidate_statement + ' [SEP] ' + candidate_context
        candidate_inputs.append( candidate_input )
    return candidate_inputs

def prepare_anchor_input(candidate_blocks):
    for candidate_block in candidate_blocks: 
        block_info = candidate_block.strip().split('\t') 
        anchor_statement = block_info[1] 
        anchor_context = block_info[2] 
        anchor_input = anchor_statement + ' [SEP] ' + anchor_context
        return anchor_input

def evaluate_candidate_blocks(model, anchor_input, candidate_inputs):
    anchor_vector = model.encode(anchor_input) 
    anchor_vector = anchor_vector.reshape((1, anchor_vector.shape[0]))
    candidate_vectors = model.encode(candidate_inputs)  
    # print(anchor_vector.shape, type(anchor_vector))
    # print(candidate_vectors.shape, type(candidate_vectors))
    distances = distance.cdist(anchor_vector, candidate_vectors, 'cosine')[0]
    similarity_scores = (1 - distances).tolist()
    # print(distances.shape, type(distances))
    # print(distances)
    # print(1 - distances)
    return similarity_scores

model = SentenceTransformer('../model_train/checkpoint-graphcodebert-eu/26300/')

test_set = os.listdir('./test_set_prepared')
test_set_result = './test_set_result'

for test_dir in test_set[:]:
    print(test_dir)
    test_files = os.listdir('./test_set_prepared/' + test_dir)
    
    if os.path.exists('./test_set_result/' + test_dir):
        print(test_dir + "created!")
        continue 
    else:
        os.makedirs('./test_set_result/' + test_dir)

    for test_file in test_files:
        print(test_file)

        try:
            with open('./test_set_prepared/' + test_dir + '/' + test_file, 'r') as fin, \
                open('./test_set_result/' + test_dir + '/' + test_file, 'w') as fout:
                test_file_lines = fin.readlines()
                # print(test_file_lines)
                if len(test_file_lines) <= 1:
                    continue 

                label = int(test_file_lines[0].strip())
                # print(label)
                fout.write(str(label) + '\n')
                anchor_function = test_file_lines[1].strip()            
                anchor_todo_lineno = int(test_file_lines[2].strip())
                anchor_todo_comment = test_file_lines[3].strip()
                fout.write(anchor_function + '\t' + str(anchor_todo_lineno) + '\t' + anchor_todo_comment + '\n')
                
                candidate_function = test_file_lines[4].strip()
                candidate_todo_lineno = int(test_file_lines[5].strip())
                candidate_todo_comment = test_file_lines[6].strip()
                fout.write(candidate_function + '\t' + str(candidate_todo_lineno) + '\t' + candidate_todo_comment + '\n')
                candidate_blocks = test_file_lines[7:]
                anchor_input = prepare_anchor_input(candidate_blocks)
                candidate_inputs = prepare_candidate_inputs(candidate_blocks)
                similarity_scores = evaluate_candidate_blocks(model, anchor_input, candidate_inputs)

                assert len(candidate_blocks) == len(similarity_scores)

                for test_block, similarity_score in zip(candidate_blocks, similarity_scores): 
                    # print("======================")
                    # print(test_block)
                    # block_similarity = evaluate_candidate_block(model, test_block)
                    # print(block_similarity)
                    fout.write( test_block.strip() + '\t' + str(similarity_score) + '\n')
            # break
        # break
        except Exception as e:
            print(e)
            continue 

print("Finished!")

