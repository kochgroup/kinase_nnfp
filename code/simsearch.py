from utility import *
from sklearn.metrics.pairwise import cosine_similarity
import os
import argparse

parser = argparse.ArgumentParser(description="Generate NNFP")
parser.add_argument("input",nargs = "?",default="../data/nnfp_output.csv",type = str,help="Path to the input file.")
parser.add_argument("-q", "--query", type= int,nargs='+',help="Index of Query to peform similarity search for.")
args = parser.parse_args()


path_to_save = "/".join(args.input.split("/")[:-1])
if not os.path.exists(path_to_save+'/simsearch_results'):
    os.makedirs(path_to_save+'/simsearch_results')

data = pd.read_csv(args.input)
fps =data.iloc[:,1:]
for query in args.query:
    if np.sum(fps.iloc[query,:].isna())>0:
        print("Query "+str(query)+  " does not have a valid fingerpint")
        break
    
    simsearch_results=cosine_similarity(fps.iloc[query,:].values.reshape(1,-1),fps.dropna())
    simsearch_results=pd.DataFrame({"smiles": data.dropna().smiles, "similarity":simsearch_results.reshape(-1)}).sort_values("similarity", ascending=False)
    simsearch_results.to_csv(path_to_save+"/simsearch_results/query_"+str(query)+ ".csv")
    