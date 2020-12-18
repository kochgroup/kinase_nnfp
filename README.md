# Kinase Specifc Fingerprints

![](fp_gen_3.png)

This Repository accopmanys our work on:
"Using Domain-Specific Fingerprints Generated Through Neural Networks to Enhance Ligand-based Virtual Screening."

https://doi.org/10.26434/chemrxiv.12894800.v1


The provided code can be used to generate Molecular Fingerprints that are specific to Kinases. 
While in the paper we explore many different architectures, here we only use a MLP trained for multitask prediction to generate the neural fingerprints. 
This selection was made due to the fact that is was the best perfoming fingerprint.


# Requirements

* Python 3.7
* Pytorch 1.6
* rdKit 2019.03.4

A yml file containing all requirements is provided. This can be easily setup using conda.


# Installation 

1. Download the Repository

2. Create and Activate Conda Environment:
    Navigate to the Folder containing the environment.yml
    ```
    conda env create -f environment.yml
    conda activate get_nnfp_env
    ```
# Generate Fingerprints
You can use a csv file containing a column with SMILES strings as input to our model.
Naviagte to `*your path*/kinase_nnfp/code` and run:

```
python get_fp.py ../data/example_data.csv -s smiles
```
`smiles` is the name of the column containing the SMILES strings.

You can also provide the Index of the column containing the SMILES. 
```
python get_fp.py ../data/example_data.csv -s 0
```
If you do not have a header add the `-n` flag

```
python get_fp.py ../data/example_data.csv -s 0 -n
```


