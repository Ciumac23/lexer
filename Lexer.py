import os
import sys
import itertools
class DFA:
    def __init__(self, _abc, _start, _end, _transitions, _name):
        self.abc = _abc
        self.start = _start
        self.name = _name
        self.end = _end
        self.transitions = _transitions
        self.current_state = 0
        self.sinked = False
        self.token = ""
        self.final_token = ""
        self.final_step = 0
        self.crt_step = 0
    def get_transitions(self):
        return self.transitions
    def get_start(self):
        return self.start
    def get_end(self):
        return self.end
    def get_abc(self):
        return self.abc
    def get_name(self):
        return self.name
    def get_crt_state(self):
        return self.current_state
    def get_token(self):
        return self.token
    def get_final_states(self):
        return self.end
    def get_final_token(self):
        return self.final_token
    def get_crt_step(self):
        return self.crt_step
    def get_final_step(self):
        return self.final_step
    def set(self, name, state):
        self.token = name
        self.crt_step = state
        self.current_state = state
        self.final_token = name
        self.sinked = False
        self.final_step = state
    def print_dfa(self):
        print("Alpha: ", self.abc, len(self.abc))
        print("Name: ", self.name)
        print("Start: ", self.start)
        print("Trans: ", self.transitions)
        print("End: ", self.end)
        print("Token: ", self.final_token)
        print("Steps: ", self.final_step)
    def reset_dfa(self):
        self.current_state = 0;
        self.sinked = False

def parse_tokens(tokens, dfa_list):
    if len(tokens) == 0:
        return
    if len(tokens[0]) == 0:
        alpha = ' '
    else:
        alpha = tokens[0]
    if tokens[0] == "\\n":
        alpha = '\n'
    token_name = tokens[1]
    init_state = tokens[2]
    transitions = dict()
    start = 3
    while tokens[start] != "\n" and ',' in tokens[start]:
        t = tokens[start].split(',')
        if len(t[1]) == 3 and t[1][1] != ' ':
            transitions[(t[0], t[1][1])] = t[2]
        elif len(t[1]) == 4:
            transitions[(t[0], '\n')] = t[2]
        else:
            transitions[(t[0], ' ')] = t[2]
        start += 1
    final_states = list(map(int,filter(None,tokens[start].split(" "))))
    dfa_list.append(DFA(alpha, init_state, final_states, transitions, token_name))
    parse_tokens(tokens[start+2:], dfa_list)

def free_dfa(dfa_list):
    for _dfa in dfa_list:
        _dfa.set("", 0)
def choice(dfa_list):
    # retuns dfa with maximum length of final token
    if len(dfa_list) == 0:
        return None
    return max(dfa_list, key = lambda x: x.get_final_token())
def analize(char, dfa):    
    # check if character is in the dfa's alphabet
    # check for respective transition from 
    # current state and with current char
    if char in dfa.get_abc() and ((str(dfa.get_crt_state()), char) in dfa.get_transitions().keys()):
        # if there is a transition save the current char in final token
        # inc current step of dfa
        # update the current state of the dfa
        dfa.current_state = dfa.get_transitions()[(str(dfa.get_crt_state()), char)]
        dfa.token += char
        dfa.crt_step += 1
        if int(dfa.get_crt_state()) in dfa.get_final_states():
            dfa.final_token = dfa.token
            dfa.final_step = dfa.crt_step
    else:
        dfa.sinked = True
def compute_pattern(input, dfa_list, final_list):
    if len(input) == 0:
        return ""
    # free all info inside dfas
    free_dfa(dfa_list)
    # traverse each character of pattern
    for i in range(len(input)):
        # traverse all dfas from the Lexer and check wich one has a match
        for dfa in dfa_list:
            if dfa.sinked is not True:
                analize(input[i], dfa)
    # pick up the dfa with longest token
    dfa = choice(dfa_list)
    return (dfa.get_name()+ " "+ dfa.get_final_token() + "\n") + "" + compute_pattern(input[int(dfa.final_step):], dfa_list, final_list)
def runlexer(lexer, finput, foutput):
    # init structures for next work
    _dfa_list = []
    _final_dfas = []
    string = ""
    # read from 2 diff files dfa and pattern
    with open(lexer) as dfa_f:
        lines = dfa_f.readlines()
    with open(finput) as pattern_f:
        pattern = pattern_f.readlines()
    new_pattern = ''.join(map(str, pattern))
    pattern_f.close()
    dfa_f.close()
    # parse input string and convert into list of dfas
    strip_words = list(map(lambda x: x.strip("\n") if x != "\n" else "\n", lines))
    # recursivly parse string into dfas
    parse_tokens(strip_words, _dfa_list)
    string = compute_pattern(new_pattern, _dfa_list, _final_dfas)
    new_string = string.replace("\n\n", "\\n\n")
    with open(foutput, "w") as f:
        f.write(new_string.strip())
    f.close()
if __name__ == "__main__":
    l = sys.argv[1:]
    runlexer(l[0], l[1], l[2])