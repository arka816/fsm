def parseDFA(filename = "demo.fsm"):
    f = open(filename, 'r')
    states, alphabets = [int(item) for item in f.readline().strip().split(" ")]
    transition_table = dict()
    for i in range(states):
        row = [int(item) for item in f.readline().strip().split()]
        transition_table[i] = row
        
    initial_state = int(f.readline().strip())
    final_states = set([int(item) for item in f.readline().strip().split(" ")])
    return states, alphabets, transition_table, initial_state, final_states


def parseMealy(filename = "mealy.fsm"):
    f = open(filename, 'r')
    states, alphabets = [int(item) for item in f.readline().strip().split(" ")]
    transition_table = dict()
    for i in range(states):
        row = [int(item) for item in f.readline().strip().split()]
        transition_table[i] = row
    output_table = dict()
    for i in range(states):
        row = [int(item) for item in f.readline().strip().split()]
        output_table[i] = row
        
    state_transition_table = dict()
    for i in range(states):
        state_transition_table[i] = list(zip(transition_table[i], output_table[i]))
    return states, alphabets, state_transition_table


def parseIncompleteMealy(filename = "C:\\Users\\arkap\\OneDrive\\Documents\\summer 21\\fsm-minimization\\fsm\\incomplete_mealy.fsm"):
    f = open(filename, 'r')
    states, alphabets = [int(item) for item in f.readline().strip().split(" ")]
    transition_table = dict()
    for i in range(states):
        row = [None if item == 'X' else int(item) for item in f.readline().strip().split()]
        transition_table[i] = row
    output_table = dict()
    for i in range(states):
        row = [None if item == 'X' else int(item) for item in f.readline().strip().split()]
        output_table[i] = row
        
    state_transition_table = dict()
    for i in range(states):
        state_transition_table[i] = list(zip(transition_table[i], output_table[i]))
    return states, alphabets, state_transition_table
