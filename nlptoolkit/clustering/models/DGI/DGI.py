# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 10:58:01 2019

@author: WT
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

class GCN(nn.Module):
    def __init__(self, X_size, args, bias=True): # X_size = num features
        super(GCN, self).__init__()
        self.weight = nn.parameter.Parameter(torch.zeros(size=(X_size, args.hidden_size_1)))
        var = 2./(self.weight.size(1) + self.weight.size(0))
        self.weight.data.normal_(0, var)
        
        if bias:
            self.bias = nn.parameter.Parameter(torch.zeros(args.hidden_size_1))
            self.bias.data.normal_(0, var)
        else:
            self.register_parameter("bias", None)
        
    def forward(self, X, A_hat): ### 1-layer GCN architecture
        X = torch.mm(X, self.weight)
        if self.bias is not None:
            X = (X + self.bias)
        X = F.relu(torch.mm(A_hat, X))
        return X
    
class GIN(nn.Module):
    def __init__(self, X_size, n_nodes, A_hat, cuda, args, bias=True): # X_size = num features
        super(GIN, self).__init__()
        self.X_size = X_size
        self.n_nodes = n_nodes
        self.dum = torch.ones(size=(1, self.n_nodes))
        
        self.I = torch.eye(self.n_nodes, self.n_nodes)
        self.A_hat = torch.tensor(A_hat, requires_grad=False).float()
        if cuda:
            self.A_hat = self.A_hat.cuda()
            self.I = self.I.cuda()
            self.dum = self.dum.cuda()
            
        self.diag_A = torch.diag(self.A_hat.diag())
        self.off_diag_A = self.A_hat - self.diag_A
        
        self.e1 = nn.parameter.Parameter(torch.zeros(size=(1, 1))) # size=(self.n_nodes, 1)
        var = 2./(self.e1.size(1) + self.e1.size(0))
        self.e1.data.normal_(0, var)
        self.mlp1 = nn.Linear(self.X_size, self.X_size, bias=bias)
        
        self.e2 = nn.parameter.Parameter(torch.zeros(size=(1, 1))) # size=(self.n_nodes, 1)
        var2 = 2./(self.e2.size(1) + self.e2.size(0))
        self.e2.data.normal_(0, var2)
        self.mlp2 = nn.Linear(self.X_size, self.X_size, bias=bias)
        
        self.fc1 = nn.Linear(self.X_size, args.num_classes, bias=bias)
        
    def forward(self, X): ### 2-layer GIN architecture
        hv = torch.mm(self.diag_A, X)
        hu = torch.mm(self.off_diag_A, X)
        
        X = torch.mm((torch.diag((self.dum*self.e1).squeeze()) + self.I), hv) + hu
        X = self.mlp1(X)
        
        hv = torch.mm(self.diag_A, X)
        hu = torch.mm(self.off_diag_A, X)
        X = torch.mm((torch.diag((self.dum*self.e2).squeeze()) + self.I), hv) + hu
        X = self.mlp2(X)
        return self.fc1(X)
    
class DGI(nn.Module):
    def __init__(self, X_size, args, bias=True):
        super(DGI, self).__init__()
        self.encoder = GCN(X_size, args, bias=bias)
        self.D_weight = nn.parameter.Parameter(torch.zeros(size=(args.hidden_size_1,\
                                                                 args.hidden_size_1))) # features X features
         
    def summarize_patch(self, X):
        X = torch.sigmoid(X.mean(dim=0))
        return X
    
    def forward(self, X, A_hat, X_c):
        X = self.encoder(X, A_hat) # nodes X features
        X_c = self.encoder(X_c, A_hat) # nodes X features
        s = self.summarize_patch(X) # s = features
        fac = torch.mm(self.D_weight, s.unsqueeze(-1)) # fac = features X 1
        
        pos_D = []
        for i in range(X.shape[0]):
            pos_d_i = torch.sigmoid(torch.mm(X[i, :].unsqueeze(0), fac))
            pos_D.append(pos_d_i)
        pos_D = torch.stack(pos_D, dim=0).squeeze()
        
        neg_D = []
        for i in range(X_c.shape[0]):
            neg_d_i = torch.sigmoid(torch.mm(X_c[i, :].unsqueeze(0), fac))
            neg_D.append(neg_d_i)
        neg_D = torch.stack(neg_D, dim=0).squeeze()
        return pos_D, neg_D