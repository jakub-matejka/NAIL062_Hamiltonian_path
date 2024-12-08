## Problem description

Hamiltonian Path problem decides if a directed (or undirected, if you add the edges in both directions) graph, G, contains a Hamiltonian path, a path that visits every vertex in the graph exactly once. The problem may specify the start and end of the path.

the program takes only files as input
on first line is specified the number of vertecies of the graph and then optionaly s and/or e followed by the vertex that is supposed to be first / last
the following lines are edges coming from the vertex that is on the line first

```
2 3 1    - means there are two edges from vertex 2, one to vertex 3 and other to vertex 1
```

An examples of a valid input format is:

```
6 e 1
1 2
2 4 3 
3 2 
4 3 1
5 1 2 3 
6 2 3 4 5
```

```
3 s 3 e 1
1 2 3
2 1 3 
3 2 
```

```
4 
1 2 3 4
4 1 3 
3 2 
```

if there exists hamiltonian path it will write it out like this:
4 -> 1 -> 3 -> 2

## Encoding
    pouzijeme znaceni jako kdyz chceme uporadani vrcholu, tedy p_i_j kde i-ty vrchol na j-te pozici
    mame n pozic pro cestu o n vrcholech tedy n*n znaku
    postupně p_1_1, p_1_2, ... p_2_1
    zakladni podminky na hamiltonovu cestu:
    na kazde pozici je alespon jeden vrchol a na 1 pozici je max 1 vrchol
    kazdy bod bude v ceste jednou (alespon na jedne pozici), max jednou (jen na jedne)
    pak přidáme podminky z naseho input.in
    pokud vrcholy nejsou spojene hranou tak nebudou v ceste za sebou
    tedy pokud z X nevede do Y strana přidáme -p_X_k a -p_Y_k+1
    nakonec přidáme (pokud jsou nastavene) starting point tedy p_s_1 a nezávisle na tom end p_e_n jako true

## Programing doc

this repo contains the unix binary for glucose-syrup and glucose-syrup.exe
it can run both, for the unix there is function that uses wsl but the program uses the .exe version

## User documentation

Basic usage: 
```
HamiltonianPath.py [-h] [-i INPUT] [-o OUTPUT] [-s SOLVER] [-v {0,1}] [-c {0,1}]
```
or better yet, in visual studio

Command-line options:

* `-h`, `--help` : Show a help message and exit.
* `-i INPUT`, `--input INPUT` : The instance file. Default: "input.in".
* `-o OUTPUT`, `--output OUTPUT` : Output file for the DIMACS format (i.e. the CNF formula).
* `-s SOLVER`, `--solver SOLVER` : The SAT solver to be used.
*  `-v {0,1}`, `--verb {0,1}` :  Verbosity of the SAT solver used.
* `-c {0,1}`, `--cnf_print {0,1}` :  1 - prints the cnf to output as well

## Example instances

* `splnitelny_long.in`
* `splnitelny_small.in`
* `nesplnitelny_small.in`

## Experiments
the splnitelny_long.in by měl trvat víc než 10 s testoval jsem víckrát a dostal jem 16, 13, 3, 12, 6, 5 sekund 3krát víc jak 10 ale 3krát méně
