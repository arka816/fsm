def parseFSM(filename = "demo.fsm"):
    f = open(filename, 'r')
    states, alphabets = [int(item) for item in f.readline().strip().split(" ")]
    transition_table = dict()
    for i in range(states):
        row = [int(item) for item in f.readline().strip().split()]
        transition_table[i] = row
        
    initial_state = int(f.readline().strip())
    final_states = set([int(item) for item in f.readline().strip().split(" ")])
    return states, alphabets, transition_table, initial_state, final_states