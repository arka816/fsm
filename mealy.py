"""
 * author: Arkaprava Ghosh
 * mealy machine minimization
 * for completely specified machines
 
 * this script also generates the
 * verilog code for the reduced automata
"""

from fsm_parser import parseMealy

states, alphabets, state_transition_table = parseMealy()

P_prev = [set(range(states))]

for c in range(alphabets):
    d=dict()
    for state in range(states):
        i = state_transition_table[state][c][1]
        if i in d:
            d[i].append(state)
        else:
            d[i] = [state]
    if len(d) > 1:
        break

P_curr = [set(val) for key, val in d.items()]      

while len(P_prev) != len(P_curr):
    P = []
    for eq_class in P_curr:
        for c in range(alphabets):
            d = dict()
            for state in eq_class:
                next_state = state_transition_table[state][c][0]
                for i in range(len(P_curr)):
                    if next_state in P_curr[i]:
                        if i in d:
                            d[i].append(state)
                        else:
                            d[i] = [state]
                        break
            if len(d) != 1:
                break
        for key, value in d.items():
            P.append(set(value))
    P_prev = P_curr
    P_curr = P
    
print(P)                

# REMOVE EQUIVALENT STATES
Q_minimal = set([])

for eq_class in P:
    l = list(eq_class)
    Q_minimal.add(l[0])
    for eq_state in l[1:]:
        del state_transition_table[eq_state]
        
# MODIFY TRANSITION TABLE
for key, value in state_transition_table.items():
    for i in range(alphabets):
        for eq_class in P:
            if value[i][0] in eq_class:
                value[i] = (min(eq_class), value[i][1])
                
print("states: ", Q_minimal)
print(state_transition_table)
                