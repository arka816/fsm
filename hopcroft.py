"""
 * author: Arkaprava Ghosh
 * hopcroft algorithm
 * finite automata minimization
 * for completely specified machines
 * without output
 
 * hopcroft's algorithm is based on
 * partition refinement
 * subsets are generated as
 * equivalence classes based on
 * myhill-nerode equivalence relation
 
 * this script also generates the
 * verilog code for the reduced automata
"""

from fsm_parser import parseDFA

states, alphabets, transition_table, initial_state, final_states = parseDFA()

## REMOVE UNREACHABLE STATES
Q = set(range(states))
reachable_states = set([initial_state])
new_states = set([initial_state])

while len(new_states) > 0:
    temp = set([])
    for q in new_states:
        for c in range(alphabets):
            temp = temp.union({transition_table[q][c]})
    new_states = temp.difference(reachable_states)
    reachable_states = reachable_states.union(new_states)
    
unreachable_states = Q.difference(reachable_states)

Q = reachable_states

for state in unreachable_states:
    del transition_table[state]
    

# MANAGE EQUIVALENT STATES
P = [final_states, Q.difference(final_states)]
W = [final_states, Q.difference(final_states)]

while len(W) > 0:
    A = W.pop(0)
    for c in range(alphabets):
        X = set([])
        for key, value in transition_table.items():
            if value[c] in A:
                X.add(key)
        for Y in P:
            if len(Y.intersection(X)) > 0 and len(Y.difference(X)) > 0:
                P.remove(Y)
                P.append(Y.intersection(X))
                P.append(Y.difference(X))
                if Y in W:
                    W.remove(Y)
                    W.append(Y.intersection(X))
                    W.append(Y.difference(X))
                else:
                    if len(Y.intersection(X)) <= len(Y.difference(X)):
                        W.append(Y.intersection(X))
                    else:
                        W.append(Y.difference(X))


# REMOVE EQUIVALENT STATES
final_states_minimal = set([])
Q_minimal = set([])

for eq_class in P:
    l = list(eq_class)
    Q_minimal.add(l[0])
    if l[0] in final_states:
        final_states_minimal.add(l[0])
    if initial_state in l:
        initial_state_minimal = l[0]
    for eq_state in l[1:]:
        del transition_table[eq_state]
        
# MODIFY TRANSITION TABLE
for key, value in transition_table.items():
    for i in range(alphabets):
        for eq_class in P:
            if value[i] in eq_class:
                value[i] = min(eq_class)
        
print("states: ", Q_minimal)
print("initial state: ", initial_state_minimal)
print('acceptable states: ', final_states_minimal)
print(transition_table)