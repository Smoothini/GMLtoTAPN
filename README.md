# Update Synthesis Problem experiments repository

## About
Welcome to the Update Synthesis Problem experiments repository!
This repository was used in order to conduct experiments for our paper.
Our experimental environment was a linux cluster with 128gb RAM, thus the user is warned there is a chance that on a normal home pc **not** all the experiments will manage to run. 

## Contents
### Network-generating files:
- **data**: Contains the original GML files downloaded from topology-zoo.org. It is also the place where the json,xml,q,tapaal and ltl files for both synthethic and topology zoo networks will be kept.
- **engines**: Contains the dtapn and netsynth verifier engines.
- **entities & utils**: Contains the logic needed in order to parse/generate networks. 
- **Pipeline.py**: python3 script which, when run, is going to call all the necessary functionality in order to generate the dtapn xml's and q's, and netsynth ltl's in order for the tests to be run.
- **21122020.zip**: zip file containing this repository, setup in a way that when the `./run_experiments.sh` command is run in the root folder, the experiments present in the paper will be re-conducted.
### Network-solving scripts:
- **purge.sh**: bash script that removes previously generated files from the data folder.
- **solve_synthethic_dtapn.sh**: bash script that solves synthethic networks using the dtapn verifier engine. By using this script, the RAM usage can easily spike up due to the high amount of computation involved. 
- **solve_synthethic_netsynth.sh**: bash script that solves synthethic networks using the netsynth engine.
- **solve_synthethic.sh**: bash script that chains the network building Pipeline with the previous three scripts.
- **solve_zoo_dtapn.sh**: bash script that solves topology zoo networks using the dtapn verifier engine.
- **solve_zoo_netsynth.sh**: bash script that solves topology zoo networks using the netsynth engine.
- **solve_zoo.sh**: bash script that chains the network building Pipeline with the two previously mentioned scripts.
- **solve_all.sh**: bash script that chains `./solve_synthethic.sh` and `./solve_zoo.sh`



## Experimental Flow
Based on whether we try to solve topology zoo or synthetic networks, the flow is different.
### Topology Zoo
1. GML files are parsed into JSON files in order to compute initial and final routes. Properties such as reachability and waypoint are also appended to the JSON file, based on the network's configuration.
2. Based on the JSON file, the files required to verify the network's properties using dtapn and netsynth are generated.
### Synthethic Networks
1. Using predetermined algorithms, synthethic networks for our 3 different cases are generated and parsed into JSON files. All the networks are correct by construction. 
2. The results from the aforementioned algorithms together with the JSON files are used in order to generate the required files to verify a network's properties.


## Usage
Due to the high amount of data in this repository's history, if one wishes to clone the branch instead of downloading the mentioned zip file, it it highly recomended to use the clone command along with the depth tag such as: `git clone --depth 1 https://github.com/Smoothini/GMLtoTAPN.git`.
In order to reproduce the experiments from the paper, the only requirement is to be on a linux-based operating system and to have the **networkx** library installed for python3 in order to be able to read and parse GML files using python. Afterwards, all the required files are present here and the experiments can be started by running `./run_all.sh` from a terminal opened in the root of the folder. 