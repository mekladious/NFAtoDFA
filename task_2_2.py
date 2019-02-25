import argparse
import re
import string

class DFA:
    def __init__(self, nfa_states, name):
        self.name = name
        self.nfa_states = nfa_states

def epsilon_closure(p_nfa_states, transitions):
    for nfa_s in p_nfa_states:
        for t in transitions:
            if t[0] == nfa_s and t[1] == ' ' and not t[2] in p_nfa_states :
                p_nfa_states.append(t[2])
    return p_nfa_states

def nfa_to_dfa(states, alpha, start, goal, transitions):
    dfa_states = []
    dfa_trans = []
    dfa_goals = []
    states_tmp = []
    states_tmp.append(start)
    states_tmp = epsilon_closure(states_tmp, transitions)
    if goal in states_tmp:  
        dfa_goals.append('A')  
    dfa_states.append(DFA(states_tmp, string.ascii_uppercase[len(dfa_states)]))
    states_tmp = []
    duplicate = False
    dead_state = DFA([], "DEAD")
    for current_s in dfa_states:
        for a in alpha:
            if a != ' ':
                for s in current_s.nfa_states:
                    for t in transitions:
                        if t[0]==s and t[1]==a and not t[2] in states_tmp:
                            states_tmp.append(t[2])
                if len(states_tmp)>0:
                    states_tmp = epsilon_closure(states_tmp, transitions)
                    for state in dfa_states:
                        if set(states_tmp).issubset(set(state.nfa_states)) & set(state.nfa_states).issubset(set(state.nfa_states)):
                            name = state.name
                            duplicate = True
                            break
                    if not duplicate: 
                        name =  string.ascii_uppercase[len(dfa_states)]
                        dfa_states.append(DFA(states_tmp, name))
                        if goal in states_tmp:
                            dfa_goals.append(name)
                    dfa_trans.append((current_s.name, a, name))
                    duplicate = False
                else:
                    if dead_state not in dfa_states:
                        dfa_states.append(dead_state)
                    dfa_trans.append((current_s.name, a, dead_state.name))
            states_tmp = []
    return dfa_states, dfa_trans, dfa_goals

def main():
    
    with open(args.file, "r") as file:
        lines = file.readlines()
    states = lines[0].replace("\n","").split(',')
    alpha = lines[1].replace("\n","").split(',')
    start = lines[2].replace("\n","")
    goal = lines[3].replace("\n","")
    transitions_s = lines[4].replace("\n","")
    transitions_s_arr = transitions_s.replace(" ","").replace(",,",", ,").split('),(')
    transitions = []
    t = transitions_s_arr[0][1:].split(',')
    transitions.append((t[0],t[1],t[2]))
    for i in range(1,len(transitions_s_arr)-1):
        t = transitions_s_arr[i].split(',')
        transitions.append((t[0],t[1],t[2]))
    t = transitions_s_arr[-1][:-1].split(',')
    transitions.append((t[0],t[1],t[2]))

    dfa_states, dfa_trans, dfa_goals = nfa_to_dfa(states, alpha, start, goal, transitions)
    if ' ' in alpha:
        alpha.pop(alpha.index(' '))
    output_file = open("task_2_2_result.txt", "w+")
    output_file.write(','.join(string.ascii_uppercase[:len(dfa_states)])+'\n')
    output_file.write(','.join(alpha)+'\n')
    output_file.write('A'+'\n')
    output_file.write(','.join(dfa_goals)+'\n')
    output_file.write(str(dfa_trans).replace("\'","").replace("[","").replace("]","")+'\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?", metavar="file")

    args = parser.parse_args()

    print(args.file)

    main()