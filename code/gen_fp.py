from utility import *
import argparse

parser = argparse.ArgumentParser(description="Generate NNFP")
parser.add_argument("-i","--input",type = str,help="Path to the input file.")
parser.add_argument("-s", "--smiles",default = "smiles", help="Name or number of column containing the SMILES string.")
parser.add_argument("-t", "--header", default = "infer", action='store_const', const=None, help="Read in header")
args = parser.parse_args()


#convert colnumbers to int
try:
    args.smiles=int(args.smiles)
except:
    pass

data = pd.read_csv(args.input, nrows=1000, header=args.header)
ecfp4,index_error=get_fingerprints(data, label=args.smiles)

model = MLP([1024,1024,254, 160], 0.33)
model.load_state_dict(torch.load("../data/trained_model"))
nnfp = model(torch.tensor(ecfp4.values, dtype= torch.float))[1].detach().numpy()
nnfp[index_error,:] = np.nan
nnfp = pd.DataFrame(nnfp)

out=pd.concat([data.iloc[:,args.smiles], nnfp], axis=1)
output_path="/".join(args.input.split("/")[:-1])
out.to_csv(output_path+"/nnfp_output,csv", index=False)

