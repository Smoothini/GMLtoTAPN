# Update Synthesis Problem experiments repository

## About
Welcome to the Update Synthesis Problem experiments repository!
This repository was used in order to conduct experiments for our paper.
Our experimental environment was a linux cluster with 128gb RAM, thus the user is warned there is a chance that on a normal home pc **not** all the experiments will manage to run. 

Further information is provided in the README files present in each folder.



## Usage
Due to the high amount of past data in this repository's history, if one wishes to clone the branch instead of downloading the mentioned zip file, it it highly recomended to use the clone command along with the depth tag such as: `git clone --depth 1 https://github.com/Smoothini/GMLtoTAPN.git`.
In order to reproduce the experiments from the paper, the only requirement is to be on a linux-based operating system and to have the **networkx** library installed for python3. Afterwards, all the required files are present here and the experiments can be started by running either `./solve_zoo.sh`, either `./solve_synthethic.sh` from a terminal opened in the root of the folder. 



## Contents
### Network-generating files:
- **data**: Contains the original GML files downloaded from topology-zoo.org. It is also the place where the json,xml,q,tapaal and ltl files for both synthethic and topology zoo networks will be kept.
- **engines**: Contains the dtapn and netsynth verifier engines.
- **entities** and **utils**: Contains the logic needed in order to parse/generate networks. 
- **Generate_Zoo.py** and **Generate_Synthethic.py**: python3 scripts which, when run, are going to call all the necessary functionality in order to generate the dtapn xml's and q's, and netsynth ltl's in order for the tests to be run.
- **CSV_Synthethic.py** and **CSV_Zoo.py**: python3 scripts which compile the results obtained after solving the networks.
- **21122020.zip**: zip file containing this repository, setup in a way that when the `./run_experiments.sh` command is run in the root folder, the experiments present in the paper will be re-conducted.
### Network-solving scripts:
- **purge.sh**: bash script that removes ALL previously generated files from the data folder.
- **solve_synthethic_dtapn.sh**: bash script that solves synthethic networks using the dtapn verifier engine. By using this script, the RAM usage can easily spike up due to the high amount of computation involved. 
- **solve_synthethic_netsynth.sh**: bash script that solves synthethic networks using the netsynth engine.
- **solve_synthethic.sh**: bash script that chains the old data removal and the synthethic network building and solving pipeline. results are compiled in a CSV file.
- **solve_zoo_dtapn.sh**: bash script that solves topology zoo networks using the dtapn verifier engine.
- **solve_zoo_netsynth.sh**: bash script that solves topology zoo networks using the netsynth engine.
- **solve_zoo.sh**: bash script that chains the old data removal and the zoo topology network building and solving pipeline. results are compiled in a CSV file.


All .sh files come chmod'ed by default.




## Experimental Flow
Based on whether we try to solve topology zoo or synthetic networks, the flow is different.
### Topology Zoo
1. GML files are parsed into JSON files in order to compute initial and final routes. Properties such as reachability and waypoint are also appended to the JSON file, based on the network's configuration.
2. Based on the JSON file, the files required to verify the network's properties using dtapn and netsynth are generated.
### Synthethic Networks
1. Using predetermined algorithms, synthethic networks for our 3 different cases are generated and parsed into JSON files. All the networks are correct by construction. 
2. The results from the aforementioned algorithms together with the JSON files are used in order to generate the required files to verify a network's properties.
