# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:56:49 2019

@author: WT
"""

from utils.misc import save_as_pickle
from ASR.trainer import train_and_fit
from ASR.evaluate import infer
import logging
from argparse import ArgumentParser

logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', \
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger('__file__')

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--folder", type=str, default="train-clean-5", help="Folder containing speech files")
    parser.add_argument("--level", type=str, default="word", help="Level of tokenization (word or char)")
    parser.add_argument("--use_lg_mels", type=int, default=1, help="Use log mel spectrogram if 1, else if 0 use MFCC instead")
    parser.add_argument("--use_conv", type=int, default=1, help="Use convolution on features if 1, else if 0 don't use")
    parser.add_argument("--n_mels", type=int, default=80, help="Number of Mel bands to generate")
    parser.add_argument("--n_mfcc", type=int, default=13, help="number of MFCC coefficients")
    parser.add_argument("--n_fft", type=int, default=25, help="Length of FFT window (ms)")
    parser.add_argument("--hop_length", type=int, default=10, help="Length between successive frames (ms)")
    parser.add_argument("--max_frame_len", type=int, default=1000, help="Max audio frame length") # 3171
    parser.add_argument("--d_model", type=int, default=128, help="Transformer model dimension")
    parser.add_argument("--ff_dim", type=int, default=128, help="Feed forward layer dimension")
    parser.add_argument("--num", type=int, default=6, help="Number of layers")
    parser.add_argument("--n_heads", type=int, default=4, help="Number of attention heads")
    parser.add_argument("--batch_size", type=int, default=30, help="Batch size")
    parser.add_argument("--num_epochs", type=int, default=9000, help="No of epochs")
    parser.add_argument("--lr", type=float, default=0.0003, help="learning rate")
    parser.add_argument("--gradient_acc_steps", type=int, default=4, help="Number of steps of gradient accumulation")
    parser.add_argument("--max_norm", type=float, default=1.0, help="Clipped gradient norm")
    parser.add_argument("--model_no", type=int, default=0, help="Model ID: 0 = Transformer, 1 = LAS")
    args = parser.parse_args()
    save_as_pickle("args.pkl", args)
    
    #train_and_fit(args)
    #infer(file_path="./data/train-clean-5/19/198/19-198-0008.flac", speaker='19')
    infer()