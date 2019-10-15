# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:35:51 2019

@author: WT
"""
import os
import torch
import torch.nn as nn
import torch.optim as optim
from .models.LAS.LAS_model import LAS
from .utils import load_pickle, save_as_pickle, CosineWithRestarts, lrate
from tqdm import tqdm
import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', \
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger(__file__)

def load_model_and_optimizer(args, vocab, max_features_length, max_seq_length, cuda, pyTransformer=False):
    
    if pyTransformer:
        from .models.Transformer.py_Transformer import pyTransformer as SpeechTransformer, \
                                                        create_window_mask
    else:
        from .models.Transformer.transformer_model import SpeechTransformer, create_window_mask
    
    '''Loads the model (Speech Transformer or LAS) based on provided arguments and parameters'''
    if args.use_lg_mels == 0:
        src_vocab = 3*args.n_mfcc
    else:
        src_vocab = 3*args.n_mels
    
    if args.model_no == 0:
        logger.info("Loading SpeechTransformer...")
        net = SpeechTransformer(src_vocab=src_vocab, trg_vocab=len(vocab.w2idx), d_model=args.d_model, ff_dim=args.ff_dim,\
                                num=args.num, n_heads=args.n_heads, max_encoder_len=max_features_length, \
                                max_decoder_len=max_seq_length)
    elif args.model_no == 1:
        logger.info("Loading LAS...")
        net = LAS(listener_input_size=src_vocab, listener_hidden_size=128, output_class_dim=len(vocab.w2idx))
        
    for p in net.parameters():
        if p.dim() > 1:
            nn.init.xavier_uniform_(p)
            
    criterion = nn.CrossEntropyLoss(ignore_index=1) # ignore padding tokens
    optimizer = optim.Adam(net.parameters(), lr=args.lr, betas=(0.9, 0.98), eps=1e-9)
    scheduler = CosineWithRestarts(optimizer, T_max=args.T_max)
    
    model = SpeechTransformer if (args.model_no == 0) else LAS
    model, loaded_optimizer, loaded_scheduler, start_epoch, acc = load_state(model, args, load_best=False, load_scheduler=False)

    if start_epoch != 0:
        net = model; optimizer = loaded_optimizer; scheduler = loaded_scheduler
    if cuda:
        net.cuda()

    if args.model_no == 0:
        '''
        ## if using gaussian_masking
        g_mask1 = create_gaussian_mask(int(max_features_length/4) + 1).float()
        g_mask2 = create_gaussian_mask(440).float()
        '''
        if args.max_frame_len % 4 == 0:
            #g_mask1 = create_window_mask(int(args.max_frame_len/4), window_len=137).float()
            g_mask1 = create_window_mask(int(args.max_frame_len/4), window_len=137)
        else:
            #g_mask1 = create_window_mask(int(args.max_frame_len/4) + 1, window_len=137).float()
            g_mask1 = create_window_mask(int(args.max_frame_len/4) + 1, window_len=137)
        
        #g_mask2 = create_window_mask(net.max_decoder_len - 1, window_len=11).float();
        g_mask2 = None
        #g_mask = None
        if cuda:
            g_mask1 = g_mask1.cuda(); #g_mask2 = g_mask2.cuda()
    elif args.model_no == 1:
        g_mask1, g_mask2 = None, None
    
    return net, criterion, optimizer, scheduler, start_epoch, acc, g_mask1, g_mask2

def load_state(net, args, load_best=False, load_scheduler=False):
    """ Loads saved model and optimizer states if exists """
    base_path = "./data/"
    checkpoint_path = os.path.join(base_path,"test_checkpoint_%d.pth.tar" % args.model_no)
    best_path = os.path.join(base_path,"test_model_best_%d.pth.tar" % args.model_no)
    start_epoch, best_pred, checkpoint = 0, 0, None
    optimizer, scheduler = None, None
    if (load_best == True) and os.path.isfile(best_path):
        checkpoint = torch.load(best_path)
        logger.info("Loaded best model.")
    elif os.path.isfile(checkpoint_path):
        checkpoint = torch.load(checkpoint_path)
        logger.info("Loaded checkpoint model.")
    if checkpoint != None:
        start_epoch = checkpoint['epoch']
        best_pred = checkpoint['best_acc']
        if load_best:
            net = net.load_model(best_path)
        else:
            net = net.load_model(checkpoint_path)
        optimizer = optim.Adam(net.parameters(), lr=args.lr, betas=(0.9, 0.98), eps=1e-9)
        scheduler = CosineWithRestarts(optimizer, T_max=args.T_max)
        if load_scheduler:
            optimizer.load_state_dict(checkpoint['optimizer'])
            scheduler.load_state_dict(checkpoint['scheduler'])
        logger.info("Loaded model and optimizer.")    
    return net, optimizer, scheduler, start_epoch, best_pred

def load_results(model_no=0):
    """ Loads saved results if exists """
    losses_path = "./data/test_losses_per_epoch_%d.pkl" % model_no
    accuracy_path = "./data/test_accuracy_per_epoch_%d.pkl" % model_no
    if os.path.isfile(losses_path) and os.path.isfile(accuracy_path):
        losses_per_epoch = load_pickle("test_losses_per_epoch_%d.pkl" % model_no)
        accuracy_per_epoch = load_pickle("test_accuracy_per_epoch_%d.pkl" % model_no)
        logger.info("Loaded results buffer")
    else:
        losses_per_epoch, accuracy_per_epoch = [], []
    return losses_per_epoch, accuracy_per_epoch

def evaluate(output, labels):
    ### ignore index 1 (padding) when calculating accuracy
    idxs = (labels != 1).nonzero().squeeze()
    o_labels = torch.softmax(output, dim=1).max(1)[1]; #print(output.shape, o_labels.shape)
    if len(idxs) > 1:
        return (labels[idxs] == o_labels[idxs]).sum().item()/len(idxs)
    else:
        return (labels[idxs] == o_labels[idxs]).sum().item()

def evaluate_results(net, data_loader, cuda, g_mask1, g_mask2, create_masks, args):
    acc = 0
    print("Evaluating...")
    with torch.no_grad():
        net.eval()
        for i, data in tqdm(enumerate(data_loader), total=len(data_loader)):
            if args.model_no == 0:
                src_input, trg_input, f_len = data[0], data[1][:, :-1], data[2]
                labels = data[1][:,1:].contiguous().view(-1)
                src_mask, trg_mask = create_masks(src_input, trg_input, f_len, args)
                if cuda:
                    src_input = src_input.cuda().float(); trg_input = trg_input.cuda().long(); labels = labels.cuda().long()
                    src_mask = src_mask.cuda(); trg_mask = trg_mask.cuda()
                outputs = net(src_input, trg_input, src_mask, trg_mask, g_mask1, g_mask2)
                
            elif args.model_no == 1:
                src_input, trg_input = data[0], data[1][:, :-1]
                labels = data[1][:,1:].contiguous().view(-1)
                if cuda:
                    src_input = src_input.cuda().float(); trg_input = trg_input.cuda().long(); labels = labels.cuda().long()
                outputs = net(src_input, trg_input)
            outputs = outputs.view(-1, outputs.size(-1))
            acc += evaluate(outputs, labels)
    return acc/(i + 1)

def decode_outputs(outputs, labels, vocab):
    l = list(labels[:50].cpu().numpy())
    o = list(torch.softmax(outputs, dim=1).max(1)[1][:50].cpu().numpy())
    print("Sample Output: ", " ".join(vocab.convert_idx2w(o)))
    print("Sample Label: ", " ".join(vocab.convert_idx2w(l)))