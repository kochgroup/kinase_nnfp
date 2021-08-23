# Kinase Specifc Fingerprints

![](fp_gen_3.png)

This Repository accompanys our work on:
"Using Domain-Specific Fingerprints Generated Through Neural Networks to Enhance Ligand-based Virtual Screening."

https://pubs.acs.org/doi/10.1021/acs.jcim.0c01208?


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
# Perform a Similarity Seach based on the produced Fingerprint
If you want to use the NNFPs for a similarity search make sure that the query is in the same file as the molecules you want to screen before you generate the Fingerprints.

With `python simsearch.py *path of fingerprintfile* -q *index of the query*` the similairty search can be performed

Given you generated fingerprints for the `example_data.csv`. The following code will perform a similarity search for the query with index 0 

```
python simsearch.py ../data/nnfp_output.csv -q 0
```
You can also perform a similarity search for multiple queries by adding addtional indices.

```
python simsearch.py ../data/nnfp_output.csv -q 0 15 8 1 84
```
A new folder will be generated containing the results of the similairty search
Like in the original paper, the cosine similarity is used for the search.





