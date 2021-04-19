# FINITE STATE MACHINE MINIMIZATION

We present minimization algorithms for reducing Moore Machines, Mealy Machines and deterministic finite automata using equivalence classes.
The project also aims to produce verilog code for said minimal automata.

## Execution and test files
### for finite state machines without output
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
