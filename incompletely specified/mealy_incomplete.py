"""
 * author: Arkaprava Ghosh
 * mealy machine minimization
 * for incompletely specified machines
 
 * using merger tables
 * and compatibilty graphs
 
 * this script also generates the
 * verilog code for the reduced automata
"""

from fsm_parser import parseIncompleteMealy

states, alphabets, state_transition_table = parseIncompleteMealy()

def generateMergerTable():
    mergerTable = [[False for j in range(states - 1)] for i in range(states - 1)]
    for i in range(states - 1):
        for j in range(i + 1):
            flag = True
            for k in range(alphabets):
                output_i, output_j = state_transition_table[i+1][k][1], state_transition_table[j][k][1]
                if output_i != None and output_j != None and output_i != output_j:
                    flag = False
                    break
            if not flag:
                mergerTable[i][j] = False
                continue
            else:
                dependencies = []
                for k in range(alphabets):
                    state_i, state_j = state_transition_table[i+1][k][0], state_transition_table[j][k][0]
                    if state_i != None and state_j != None and state_i != state_j:
                        if (i+1, j) != (state_i, state_j) and (i+1, j) != (state_j, state_i):
                            dependencies.append((max(state_i, state_j), min(state_i, state_j)))
                if len(dependencies) == 0:
                    mergerTable[i][j] = True
                else:
                    mergerTable[i][j] = dependencies
                    
    return mergerTable
    
mergerTable = generateMergerTable()