## DTapn

DTapn is the verifier engine used by TAPAAL. In order to augment the execution speed, we bypass TAPAAL's GUI by running the engine through a bash terminal. 

The version of DTAPN used here was compiled from [here](https://github.com/TAPAAL/verifydtapn/tree/strategy_output/src/DiscreteVerification) and it is a in-development version that also supports outputting the strategy it find in case the property/properties is/are verified.

The command used to run it is

`./verifydtapn-linux64 -k $tokens -o 1 -m 0 -z file.txt file.xml file.q`

where 
- `$tokens` is the number of tokens we desire to use in the verification,
- `file.txt` is the strategy output after solving the problem,
- `file.xml` is the network in a format that is supported by DTAPN,
- `file.q` is the file containing the query we wish to verify.

## Netsynth

Netsynth is the verifier engine used to solve the problem with the aid of ltl files. By construction, an xml+q "data tuple" will contain the same exact network as its corresponding ltl file.

The command used to run this tool in the bash terminal is

`./netsynth solve file.ltl`

where `file.ltl` is the ltl representation of the network in cause.

## Batch processing

In order to chain-execute networks, multiple bash files encapsulating the commands above were created in the root directory. They all respect the following structure:

`{ time timeout -k 5s xm command ;} 2> result.txt`

where 
- `xm` represents the maximum time limit we want a single network solving to take, x being the amount of minutes. Eg. 3m 5m 10m etc..
- `5s` is used with the timeout command to that if a network goes over the `xm` time limit, at most 5 seconds later a linux kill process command will be issued and the next experiment will be started if there are any left.
- `command` represents either the dtapn either the netsynth solving command.
- `result.txt` is going to store the execution time of the test in cause. If any error occurs, such as RAM shortage or parsing issues, that will also be stored here.

The structure above is further encapsulated in `for` loops which iterate through the data contents we specify.