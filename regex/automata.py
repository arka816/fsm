import networkx as nx
import matplotlib.pyplot as plt

# e-nfa for regex compilation

class ENFA:
    def __init__(self, states, initial_state, accepting_state, transitions) -> None:
        # storing nfas as graphs (transition diagrams)
        self.states = states
        self.initial_state = initial_state
        self.accepting_state = accepting_state
        self.transitions = transitions

    def simplify_states(self):
        # convert hashed state ids to integers for simplicity
        states = list(self.states)
        transfer_matrix = {states[i] : i for i in range(len(states))}

        self.states = set([transfer_matrix[state] for state in self.states])
        self.transitions = [(transfer_matrix[start], transfer_matrix[end], symbol) for start, end, symbol in self.transitions]
        self.initial_state = transfer_matrix[self.initial_state]
        self.accepting_state = transfer_matrix[self.accepting_state]

    def draw_automata(self):
        edges = [(start, end) for start, end, _ in self.transitions]
        edge_labels = {(start, end) : symbol for start, end, symbol in self.transitions}
        G = nx.DiGraph()
        G.add_edges_from(edges)
        pos = nx.spring_layout(G)
        plt.figure()
        nx.draw(
            G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='pink', alpha=0.9,
            labels={node: node for node in G.nodes()}
        )
        nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels=edge_labels,
            font_color='red'
        )
        plt.axis('off')
        plt.title('ε-NFA')
        plt.savefig('ε-NFA.png', format='png')


    def e_close(self, state):
        # returns the ECLOSE subset of states corresponding to given state
        stack = [state]
        visited = [False] * len(self.states)
        
        while len(stack) > 0:
            curr = stack.pop()
            visited[curr] = True

            for transition in self.transitions:
                if transition[0] == curr and transition[2] == 'ε' and visited[transition[1]] == False:
                    stack.append(transition[1])

        return [state for state in self.states if visited[state]]

    def traverse_rec(self, state, string, visited):
        if len(string) == 0:
            if state == self.accepting_state:
                return True
        if visited[state][len(string)] == True:
            return False
        visited[state][len(string)] = True
        flag = False
        for child in range(len(self.states)):
            symbol = self.adj_mat[state][child]
            if symbol == None:
                continue
            elif symbol == 'ε':
                flag = self.traverse_rec(child, string, visited)
            else:
                if len(string) > 0 and string[0] == symbol:
                    flag = self.traverse_rec(child, string[1:], visited)
                else:
                    return False
            if flag:
                break
        return flag
        

    def traverse(self, string):
        # no point in traversing the same state twice
        # with the same string
        self.adj_mat = [[None for i in range(len(self.states))] for j in range(len(self.states))]
        for start, end, symbol in self.transitions:
            self.adj_mat[start][end] = symbol
        visited = [[False for i in range(len(string) + 1)] for j in range(len(self.states))]
        flag = self.traverse_rec(self.initial_state, string, visited)
        return flag
        

    def eliminate_e(self):
        # eliminate ε transitions and convert into a DFA
        pass

    
def merge_union(id, automata):
    # order of automata unimportant
    initial_state = str(id) + 'i' 
    accepting_state = str(id) + 'a'

    states = set([initial_state, accepting_state])
    transitions = []

    for automaton in automata:
        states = states.union(automaton.states)
        transitions.append((initial_state, automaton.initial_state, 'ε'))
        transitions += automaton.transitions
        transitions.append((automaton.accepting_state, accepting_state, 'ε'))

    return ENFA(states, initial_state, accepting_state, transitions)

def merge_concat(id, automata):
    # order of automata important
    if len(automata) == 1:
        return automata[0]
    
    initial_state = automata[0].initial_state
    accepting_state = automata[-1].accepting_state
    states = set()
    transitions = []

    for i in range(len(automata)):
        automaton = automata[i]
        states = states.union(automaton.states)
        transitions += automaton.transitions
        if i > 0:
            transitions.append((automata[i-1].accepting_state, automaton.initial_state, 'ε'))

    return ENFA(states, initial_state, accepting_state, transitions)


def merge_star(id, automata):
    if len(automata) != 1:
        raise Exception('kleine star can have one and only one as the number of argument automata')

    automaton = automata[0]
    initial_state = str(id) + 'i' 
    accepting_state = str(id) + 'a'

    states = set([initial_state, accepting_state]).union(automaton.states)
    transitions = automaton.transitions + [
        (initial_state, automaton.initial_state, 'ε'),
        (automaton.accepting_state, automaton.initial_state, 'ε'),
        (automaton.accepting_state, accepting_state, 'ε'),
        (initial_state, accepting_state, 'ε')
    ]

    return ENFA(states, initial_state, accepting_state, transitions)
