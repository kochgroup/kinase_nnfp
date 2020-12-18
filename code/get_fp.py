from utility import *
import os
import argparse

parser = argparse.ArgumentParser(description="Generate NNFP")
parser.add_argument("input",type = str,help="Path to the input file.")
parser.add_argument("-s", "--smiles",default = "smiles", help="Name or number of column containing the SMILES string.")
parser.add_argument("-n", "--no_header", default = "infer", action='store_const', const=None, help="Read in header")
args = parser.parse_args()


    
    
data = pd.read_csv(args.input, header=args.no_header)

#convert colnumbers to int
try:
    args.smiles=int(args.smiles)
except:
    if (type(args.smiles) == str) & (args.no_header is None):
        print("\n ERROR: If you want to index the column containing the SMILES by name, then you need to keep the header! \n")
        exit()
    args.smiles  = np.where(data.columns== args.smiles)[0][0]




print("\nStart calculating the ECFP4 from SMILES:")
ecfp4,index_error=get_fingerprints(data, label=args.smiles)

model = MLP([1024,1024,254, 160], 0.33)
model.load_state_dict(torch.load("../data/trained_model"))

print("\nStart calculating the NNFP from ECFP4:")
nnfp = model(torch.tensor(ecfp4.values, dtype= torch.float))[1].detach().numpy()
nnfp[index_error,:] = np.nan
nnfp = pd.DataFrame(nnfp)

out=pd.concat([data.iloc[:,args.smiles], nnfp], axis=1)
output_path="/".join(args.input.split("/")[:-1])
out.to_csv(output_path+"/nnfp_output.csv", index=False)

print("Finished!\n\nOutput can be found at:\n"+ str(os.path.abspath(output_path)))