import subprocess
from argparse import ArgumentParser
import os #for wsl call
from os import path

def parse_input(file_path):
    global VERT_COUNT, STARTV, ENDV
    adj_list = {}

    STARTV = -1
    ENDV = -1

    with open(file_path, 'r') as file:
        fl = file.readline().strip().split()

        a = 0
        for i in fl:
            if a == 0:
                VERT_COUNT = int(i)
                a+= 1
            if i == 's':
                a+= 1
                if a < len(fl) and fl[a].isnumeric() : 
                    STARTV = int(fl[a])
                    a+= 1
            if i == 'e':
                a+= 1
                if a < len(fl) and fl[a].isnumeric() : 
                    ENDV = int(fl[a])
                    a+=1

        for line in file:
            line = line.strip()
            if not line:
                continue
            verts = list(map(int, line.split()))
            src = verts[0]
            adj_list[src] = verts[1:]

    return adj_list

def adjacency_to_cnf_to_file(adj_list, vert_count, file_name, print_cnf):
    #pouzijeme znacni jako kdyz chceme uporadani vrcholu, tedy pij kde i-ty vrchol na j-te pozici
    #mame n pozic pro cestu o n vrcholech tedy n*n znaku

    cnf = []
    n = vert_count
    
    # base podminky na hamiltonovu cestu

    # na kazde pozici je jen jeden vrchol
    for j in range(1, n + 1):
        clause = [j + i * n for i in range(n)]
        cnf.append(clause)

    # na pozici max 1 vrchol
    for j in range(1, n + 1):
        for i in range(n):
            for k in range(i + 1, n):
                cnf.append([-(j + i * n), -(j + k * n)])

    # kazdy bod bude v ceste jednou (alespon na jedne pozici)
    for i in range(n):
        clause = [j + i * n for j in range(1, n + 1)]
        cnf.append(clause)

    # max jednou (jen na jedne)
    for i in range(n):
        for j in range(1, n + 1):
            for k in range(j + 1, n + 1):
                cnf.append([-(j + i * n), -(k + i * n)])

    # +podminky z naseho input
    # pokud vrcholy nejsou spojene hranou tak nebudou v ceste za sebou
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j and j not in adj_list.get(i, []):
                for k in range(1,n):
                    cnf.append([-((i-1) * n + k), -((j-1) * n + (k + 1) )])

    # starting and ending point
    if STARTV > 0 and STARTV <= VERT_COUNT:
        cnf.append([1+((STARTV-1)*VERT_COUNT)])
        # print("STARTV: ", STARTV)
        # print([1+(STARTV-1)*VERT_COUNT])
    if ENDV > 0 and ENDV <= VERT_COUNT:
        # print("ENDV: ", ENDV)
        # print([VERT_COUNT*ENDV])
        cnf.append([VERT_COUNT*ENDV])

    if print_cnf:
        print("p cnf {} {}".format(VERT_COUNT * VERT_COUNT, len(cnf)))
        for clause in cnf:
            print(" ".join(map(str, clause)) + " 0")

    #save to file
    total_vars = VERT_COUNT * VERT_COUNT
    total_clauses = len(cnf)

    with open(file_name, 'w') as file:
        file.write(f"p cnf {total_vars} {total_clauses}\n")
        for clause in cnf:
            file.write(" ".join(map(str, clause)) + " 0\n")

def call_solver(output_name, solver_name, verbosity):
    solver_path = solver_name + ".exe" # running the windoews executable, not the unix binary

    cmd = [solver_path, "-model", "-verb=" + str(verbosity), output_name]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result

def call_solverWSL( output_name, solver_name, verbosity):
    #running the solver from example in WSL
    current_dir = os.path.dirname(os.path.realpath(__file__))

    solver_path = os.path.join(current_dir, solver_name)

    wsl_solver_path = solver_path.replace("C:\\", "/mnt/c/").replace("\\", "/")

    cmd = f"wsl {wsl_solver_path} -model -verb={verbosity} {output_name}"

    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result

def print_result(result):
    for line in result.stdout.decode('utf-8').split('\n'):
        print(line)                 # print the whole output of the SAT solver to stdout, so you can see the raw output for yourself

    # check the returned result
    if (result.returncode == 20):       # returncode for SAT is 10, for UNSAT is 20
        return

    # parse the model from the output of the solver
    # the model starts with 'v'
    model = []
    for line in result.stdout.decode('utf-8').split('\n'):
        if line.startswith("v"):    # there might be more lines of the model, each starting with 'v'
            vars = line.split(" ")
            vars.remove("v")
            model.extend(int(v) for v in vars)      
    model.remove(0) # 0 is the end of the model, just ignore it

    print()
    print("##################################################################")
    print("########[ Better readable result of the Hamiltonian Path ]########")
    print("##################################################################")
    print()

    # decode the meaning of the assignment
    path = {}
    for i in range(0, VERT_COUNT):
        for j in range(0, VERT_COUNT):
            if model[i*VERT_COUNT+j] > 0:
                path[j+1] = i+1
                print(f"Vertex {i+1} is on position {j+1}")

    print()
    print("The Hamiltonian path is:")
    for i in range(1, VERT_COUNT):
        print(path[i], end=" -> ")
    print(path[VERT_COUNT])

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        default="input.in",
        type=str,
        help=(
            "The instance file."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        default="formula.cnf",
        type=str,
        help=(
            "Output file for the DIMACS format (i.e. the CNF formula)."
        ),
    )
    parser.add_argument(
        "-s",
        "--solver",
        default="glucose-syrup",
        type=str,
        help=(
            "The SAT solver to be used."
        ),
    )
    parser.add_argument(
        "-v",
        "--verb",
        default=1,
        type=int,
        choices=range(0,2),
        help=(
            "Verbosity of the SAT solver used."
        ),
    )
    parser.add_argument(
        "-c",
        "--cnf_print",
        default=0,
        type=int,
        choices=range(0,2),
        help=(
            "Verbosity of the SAT solver used."
        ),
    )
    args = parser.parse_args()

    # read input file
    adj = parse_input(args.input)

    # encode the problem to create CNF formula save it and maybe print it
    adjacency_to_cnf_to_file(adj, VERT_COUNT, args.output, args.cnf_print)

    # call the SAT solver and get the result
    result = call_solver(args.output, args.solver, args.verb)
    #result = call_solverWSL(args.output, args.solver, args.verb)

    # interpret the result and print it in a human-readable format
    print_result(result)