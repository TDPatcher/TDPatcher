from sentence_transformers import SentenceTransformer, LoggingHandler, InputExample, SentencesDataset
from sentence_transformers import models, util, datasets, evaluation, losses
import logging
import os
import gzip
import math
from torch.utils.data import DataLoader
from datetime import datetime

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])


# Some training parameters. For the example, we use a batch_size of 128, a max sentence length (max_seq_length)
# of 32 word pieces and as model roberta-base

model_name = 'graphCodeBERT'
batch_size = 8 
# max_seq_length = 256 
num_epochs = 35 

train_samples = []
with open('./anchor_samples', 'r') as af, \
    open('./positive_samples', 'r') as pf, \
    open('./negative_samples', 'r') as nf:
    for anchor_line, positive_line, negative_line in zip(af, pf, nf):
        # print(anchor_line, positive_line, negative_line)
        anchor_statement = anchor_line.strip().split('\t')[0]
        anchor_context = anchor_line.strip().split('\t')[1]
        anchor_input = anchor_statement + ' [SEP] ' + anchor_context

        positive_statement =  positive_line.strip().split('\t')[0]
        positive_context = positive_line.strip().split('\t')[1]
        positive_input = positive_statement + ' [SEP] ' + positive_context
        
        if len(negative_line.strip().split()) > 2:
            negative_statement = negative_line.strip().split('\t')[0]
            negative_context = ' '.join(negative_line.strip().split('\t')[1:])
        else:
            negative_statement = negative_line.strip().split('\t')[0]
            negative_context = negative_line.strip().split('\t')[1]

        negative_input = negative_statement + ' [SEP] ' + negative_context
        sample = InputExample(texts=[anchor_input, positive_input, negative_input])
        train_samples.append( sample )
        # print(anchor_input)
        # print(positive_input)
        # print(negative_input)
        # break

print("train_samples:", len(train_samples))
output_path = './output/'+model_name.replace("/", "-")+'-'+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

model = SentenceTransformer('microsoft/graphcodebert-base')
# model.max_seq_length = max_seq_length

train_dataset = SentencesDataset(train_samples, model)
train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=batch_size)
warmup_steps = math.ceil(len(train_dataloader) * num_epochs  * 0.1) #10% of train data for warm-up

train_loss = losses.TripletLoss(model=model)

model.fit([(train_dataloader, train_loss)], \
            epochs=num_epochs, \
            warmup_steps=warmup_steps, \
            # warmup_steps=1000, \
            output_path = output_path, \
            checkpoint_path = './checkpoint/', \
            checkpoint_save_steps = 5000, \
            # checkpoint_save_total_limit = 10, \
            use_amp=True,\
            show_progress_bar = True
            )

print("Training Finished!")
