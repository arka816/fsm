# FINITE STATE MACHINE MINIMIZATION

We present minimization algorithms for reducing Moore Machines, Mealy Machines and deterministic finite automata using equivalence classes.
The project also aims to produce verilog code for said minimal automata.

## Execution and test files
### For deterministic finite automata
The file can be executed in the terminal as:
**python file_name.py test_filename.fsm**
A sample finite state machine file namely **demo.fsm** has been provided and would be parsed as default if **test_filename.fsm** is not provided in the terminal.
It is advised to provide the complete address of the task file in the terminal during execution.
#### Format of input in demo.fsm

    8 2
    1 5
    6 2
    0 2
    2 6
    7 5
    2 6
    6 4
    6 2
    0
    2
  
  - the first line signifies the number of states and the size of the alphabet: 8 and 2 respectively
  - the next 8 lines outline the state transition table where the rows represent the states and the columns represent the letter of the alphabet
  - the next line contains the initial state, state 0 in our case
  - the last line contains a list of acceptable states, only state 2 in our case

### For Moore Machines
The file execution method is same as above.
#### Format of input in mealy.fsm

    6 2
    4 3
    5 3
    4 1
    5 1
    2 5
    1 2
    0 1
    0 0
    0 1
    0 0
    0 1
    0 0
    
  - the first line signifies the number of states and the size of the alphabet: 6 and 2 respectively
  - the next 6 lines outline the state transition table similar as above
  - the next 6 lines outline the output associated with each transition as described in the state transition table above

### For incompletely specified Moore machines
The file execution method is same as above
#### Format of input as in incomplete_mealy.fsm

    6 2
    4 1
    5 0
    4 2
    5 3
    2 2
    3 1
    0 0
    0 0
    X 0
    1 0
    1 0
    X 0

  - the first line signifies the number of states and the size of the alphabet: 6 and 2 respectively
  - the next 6 lines outline the state transition table similar as above
  - the next 6 lines outline the output associated with each transition as described in the state transition table above
  - X marks unspecified values for both states and outputs
