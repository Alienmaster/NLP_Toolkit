# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 18:04:45 2019

@author: WT
"""
from ner.trainer import train_and_fit
from ner.infer import infer
from utils.misc import save_as_pickle, load_pickle
from argparse import ArgumentParser
import logging
logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', \
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger('__file__')

if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument("--train_path", type=str, default="./data/ner/conll2003/eng.train.txt", help="Path to training data txt file")
    parser.add_argument("--test_path", type=str, default="./data/ner/conll2003/eng.testa.txt", help="Path to test data txt file (if any)")
    parser.add_argument("--num_classes", type=int, default=9, help="Number of prediction classes (starts from integer 0)")
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size")
    parser.add_argument("--tokens_length", type=int, default=128, help="Max tokens length for BERT")
    parser.add_argument("--max_steps", default=-1, type=int,
                        help="If > 0: set total number of training steps to perform. Override num_train_epochs.")
    parser.add_argument("--warmup_steps", default=0, type=int,
                        help="Linear warmup over warmup_steps.")
    parser.add_argument("--weight_decay", default=0.0, type=float,
                        help="Weight decay if we apply some.")
    parser.add_argument("--adam_epsilon", default=1e-8, type=float,
                        help="Epsilon for Adam optimizer.")
    parser.add_argument("--gradient_acc_steps", type=int, default=1, help="No. of steps of gradient accumulation")
    parser.add_argument("--max_norm", type=float, default=1.0, help="Clipped gradient norm")
    parser.add_argument("--num_epochs", type=int, default=5, help="No of epochs")
    parser.add_argument("--lr", type=float, default=5e-5, help="learning rate")
    parser.add_argument("--model_no", type=int, default=0, help="Model ID: (0: BERT, 1: XLNet)")
    parser.add_argument("--model_type", type=str, default='bert', help="Model ID: (0: BERT, 1: XLNet)")
    
    args = parser.parse_args()
    save_as_pickle("args.pkl", args)

    train_and_fit(args)
    infer(args, from_data=False)