## Problem description

Hamiltonian Path


## Encoding

    #pouzijeme znacni jako kdyz chceme uporadani vrcholu, tedy pij kde i-ty vrchol na j-te pozici
    #mame n pozic pro cestu o n vrcholech tedy n*n znaku
        # base podminky na hamiltonovu cestu

    # na kazde pozici je jen jeden vrchol
      # na pozici max 1 vrchol
      kazdy bod bude v ceste jednou (alespon na jedne pozici)
      max jednou (jen na jedne)
      +podminky z naseho input
    # pokud vrcholy nejsou spojene hranou tak nebudou v ceste za sebou
    add starting and ending point


## User documentation


Basic usage: 
```
HamiltonianPath.py [-h] [-i INPUT] [-o OUTPUT] [-s SOLVER] [-v {0,1}] [-c {0,1}]
```

Command-line options:

* `-h`, `--help` : Show a help message and exit.
* `-i INPUT`, `--input INPUT` : The instance file. Default: "input.in".
* `-o OUTPUT`, `--output OUTPUT` : Output file for the DIMACS format (i.e. the CNF formula).
* `-s SOLVER`, `--solver SOLVER` : The SAT solver to be used.
*  `-v {0,1}`, `--verb {0,1}` :  Verbosity of the SAT solver used.
* `-c {0,1}`, `--cnf_print {0,1}` :  1 - prints the cnf to output as well

## Example instances

* `graph.in`


## Experiments



