"""
 * author: Arkaprava Ghosh
 * mealy machine minimization
 * for incompletely specified machines
 
 * using merger tables
 * and compatibilty graphs
 
 * this script also generates the
 * verilog code for the reduced automata
"""

import sys
sys.path.insert(1, '../')
from fsm_parser import parseIncompleteMealy

INT_MAX = float('inf')

states, alphabets, state_transition_table = parseIncompleteMealy()

def propagateDependencies(p, q, mergerTable, propagated):
    dependencies = []
    for i in range(states - 1):
        for j in range(i + 1):
            if type(mergerTable[i][j]) == list:
                if (max(p, q), min(p, q)) in mergerTable[i][j]:
                    dependencies.append((i, j))
                    
    for i, j in dependencies:
        mergerTable[i][j] = False
        propagated[i][j] = True
        propagateDependencies(i+1, j, mergerTable, propagated)
            
    

def generateMergerTable():
    mergerTable = [[False for j in range(states - 1)] for i in range(states - 1)]
    
    # STEP 1: GENERATE MERGER TABLE FROM STATE TRANSITION TABLE
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
                    
    # STEP 2: DEPENDENCY PROPAGATION OF FALSE CELLS
    propagated = [[False for j in range(states - 1)] for i in range(states - 1)]
    for i in range(states - 1):
        for j in range(i + 1):
            if not propagated[i][j] and not mergerTable[i][j]:
                propagateDependencies(i+1, j, mergerTable, propagated)
    
    return mergerTable

def generateCompatibilityGraph(mergerTable):
    nodes = set()
    for i in range(states - 1):
        for j in range(i + 1):
            if mergerTable[i][j] != False:
                nodes.add((i+1, j))
                if type(mergerTable[i][j]) == list:
                    for d in mergerTable[i][j]:
                        nodes.add(d)
        
    nodes = list(nodes)
    l = len(nodes)
    
    compatibilityMat = [[False for j in range(l)] for i in range(l)]
    for i in range(states - 1):
        for j in range(i + 1):
            if type(mergerTable[i][j]) == list:
                x = nodes.index((i+1, j))
                for d in mergerTable[i][j]:
                    y = nodes.index(d)
                    compatibilityMat[x][y] = True
                    
    return nodes, compatibilityMat

def BFS(compatibilityMat, s):
    l = len(compatibilityMat)
    visited = [False] * (l)
    queue = []
    queue.append(s)
    visited[s] = True
    while queue:
        s = queue.pop(0)
        for i in range(l):
            if compatibilityMat[s][i] or compatibilityMat[i][s]:
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True           
    return visited

def findDisjointComponents(compatibilityMat):
    l = len(compatibilityMat)
    colors = [0] * l
    color = 0
    groups = dict()
    for i in range(l):
        if colors[i] == 0:
            color += 1
            v = BFS(compatibilityMat, i)
            for j in range(l):
                if v[j]:
                    colors[j] = color
                    if color in groups:
                        groups[color].append(j)
                    else:
                        groups[color] = [j]
    return groups

def BFSdirected(compatibilityMat, s):
    l = len(compatibilityMat)
    visited = [False] * (l)
    queue = []
    queue.append(s)
    visited[s] = True
    while queue:
        s = queue.pop(0)
        for i in range(l):
            if compatibilityMat[s][i]:
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True           
    return [i for i in range(l) if visited[i]]
    
    
mergerTable = generateMergerTable()
nodes, compatibilityMat = generateCompatibilityGraph(mergerTable)
components = findDisjointComponents(compatibilityMat)
componentSubgraphs = []

for key, component in components.items():
    subgraphs = set()
    for s in component:
        subgraphs.add(tuple(BFSdirected(compatibilityMat, s)))
    componentSubgraphs.append(subgraphs)
    
minimalSubgraph = []
minimalSubgraphLength = INT_MAX
    
def combineSubgraphs(c, componentSubgraphs, curr):
    global nodes, minimalSubgraph, minimalSubgraphLength
    if c >= len(componentSubgraphs):
        s=  set()
        for node in curr:
            s.add(nodes[node][0])
            s.add(nodes[node][1])
        if len(s) == states:
            if len(curr) < minimalSubgraphLength:
                minimalSubgraph = curr
                minimalSubgraphLength = len(curr)
        return
    combineSubgraphs(c+1, componentSubgraphs,  curr)
    for subgraph in componentSubgraphs[c]:
        combineSubgraphs(c+1, componentSubgraphs,  curr + list(subgraph))
    
combineSubgraphs(0, componentSubgraphs, [])
