from torch.nn.modules.module import Module
from torch import nn 
import torch.nn.functional as F
import math
from torch import nn
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import RDLogger
import torch
from tqdm import tqdm
import pandas as pd
import numpy as np

class MLP(torch.nn.Module):
   def __init__(self, layersize, dropout):
       super(MLP, self).__init__()
       self.hidden=nn.ModuleList()
       self.batchnorm= nn.ModuleList()
       self.dropout= dropout
       for k in range(len(layersize)-1):
           self.hidden.append(nn.Linear(layersize[k], layersize[k+1]))
           self.batchnorm.append(nn.BatchNorm1d(layersize[k+1]))
            
       
   def forward(self, x):
       for layer in range(len(self.hidden)-1):
           x = F.relu(self.hidden[layer](x))
           x= F.dropout(x, self.dropout, training=self.training)
           x= self.batchnorm[layer](x)
           
           if layer == (len(self.hidden)-2):
               #x= self.batchnorm[-2](x)
               fingerprint=x

       x= self.hidden[-1](x)        
       return(x, fingerprint)

def get_fingerprints(data, label ,bitSize_circular=1024, morgan_radius=2):
    
    index_not_convertable = []
    
    """ 
    Computes the Fingerprints from Molecules
    """
    # if label is string get colum number

    #Disable printing Warnings
    RDLogger.DisableLog('rdApp.*')  
    
    feature_matrix= pd.DataFrame(np.zeros((data.shape[0],bitSize_circular)), dtype=int) 
    
    
    for i in tqdm(range(data.shape[0])):
       try:
           feature_matrix.iloc[i,:] = np.array(AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromSmiles(data.iloc[i, label]),morgan_radius,nBits=bitSize_circular)) 
       except:
           feature_matrix.iloc[i,:] = 0
           index_not_convertable.append(i)
    RDLogger.EnableLog('rdApp.*')  
    
    if len(index_not_convertable)> 0:
        print("\n",len(index_not_convertable), " Molecules could not be read.")  
    
    
    return feature_matrix, index_not_convertable
