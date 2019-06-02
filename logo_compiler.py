#!/usr/bin/python

import sys
import re

tokens = {
    "number":       (0,r'\d+'),
    "variable":     (1,r'\$var'),
    "begin":        (2,r'\$begin'),
    "end":          (3,r'\$end'),
    "move":         (4,r'\$move'),
    "turn":         (5,r'\$turn'),
    "define":       (6,r'\$define'),
    "arg_right":    (7,r'right'),
    "arg_forward":  (8,r'forward'),
    "identifier":   (9,r'[a-zA-Z]+'),
    "oparenthesis": (10,r'\('),
    "cparenthesis": (11,r'\)'),
    "comma":        (12,r','),
    "equal":        (13,r':='),
    "plus":         (14,r'\+'),
    "minus":        (15,r'\-'),
    "comment":      (16,r'//.*'),
    "newline":      (17,r'\n'),
    "whitespace":   (18,r' ')
}

OTHER_LEXEMA = 255

error = 0
idx   = 0
llen  = 0

def print_lexema(ttype,lexema):
    found = 0
    for key in tokens:
        if tokens[key][0] == ttype:
            print "{}\tis\t{}".format(lexema,key)
            found = 1
    if found == 0:
        print "Error: {} not a token".format(lexema)

def get_token(lexema):
    ret = OTHER_LEXEMA
    for key in tokens:
        if re.match(tokens[key][1],lexema):
            ret = tokens[key][0]
    return ret

def Variables(sequence):
    global idx
    global llen

    token = get_token(sequence[idx])
    print_lexema(token,sequence[idx])
    while token == tokens["variable"][0] and idx < llen:
         idx = idx + 1
         token = get_token(sequence[idx])
         print_lexema(token,sequence[idx])
         if token == tokens["identifier"][0]:
             idx = idx + 1
         else:
             print "Error !!"
         
         token = get_token(sequence[idx])
         print_lexema(token,sequence[idx])
         if token == tokens["equal"][0]:
             idx = idx + 1
         else:
             print "Error !!"

         token = get_token(sequence[idx])
         if token == tokens["number"][0]:
             idx = idx + 1
         else:
             print "Error !!"

def Defines(sequence):
    global idx
    global llen
    
    token = get_token(sequence[idx])
    print_lexema(token,sequence[idx])
    while token == tokens["comment"][0] and idx < llen:
        idx = idx + 1
        token = get_token(sequence[idx])
        print_lexema(token,sequence[idx])
    
    if token == tokens["define"][0] and idx < llen:
        idx = idx + 1
        Variables(sequence)
    else:
        error = 1
        print "Error !!"

def Begin(sequence):
    global idx
    global llen
    token = get_token(sequence[idx])
    print_lexema(token,sequence[idx])
    if token == tokens["begin"][0] and idx < llen:
        idx = idx + 1
    else:
        print "Error !!"

def Argument(sequence):
    global idx
    global llen
    token = get_token(sequence[idx])
    print_lexema(token,sequence[idx])
    if token == tokens["arg_right"][0] or tokens["arg_forward"][0]:
        idx = idx + 1
    else:
        print "Error !!"

def Expression(sequence):
    global idx
    global llen
    token = get_token(sequence[idx])
    print_lexema(token,sequence[idx])
    if token == tokens["number"][0]:
        idx = idx + 1
    else:
        print "{} Error !!".format(sequence[idx])

def Behaviour(sequence):
    global idx
    global llen
    token = get_token(sequence[idx])
    print_lexema(token,sequence[idx])
    while token == tokens["move"][0] or token == tokens["turn"][0]:
        idx = idx + 1
        token = get_token(sequence[idx])
        print_lexema(token,sequence[idx])
        if token == tokens["oparenthesis"][0]:
            idx = idx + 1
            Argument(sequence)
            token = get_token(sequence[idx])
            print_lexema(token,sequence[idx])
            if token == tokens["comma"][0]:
                idx = idx + 1
                Expression(sequence)
                token = get_token(sequence[idx])
                print_lexema(token,sequence[idx])
                if token == tokens["cparenthesis"][0]:
                    idx = idx + 1
                else:
                    print "Error !!"
            else:
                print "Error !!"
        else:
            print "Error !!"
        token = get_token(sequence[idx])

def End(sequence):
    global idx
    global llen
    token = get_token(sequence[idx])
    print_lexema(token,sequence[idx])
    if token != tokens["end"][0]:
        print "Error !!"

def Compile(sequence):
    global llen
    global idx
    llen = len(sequence)
    idx = 0
    Defines(sequence)
    Begin(sequence)
    Behaviour(sequence)
    End(sequence)

def main():
    contents = []
    with open(sys.argv[1], 'r') as f:
        contents = f.read()
        contents = re.split(r'(\n|[ ]|//.*|\d+|\$[a-zA-Z]+|[a-zA-Z]+|\(|\))',contents)
    
    while '' in contents: contents.remove('')
    while ' ' in contents: contents.remove(' ')
    while '\n' in contents: contents.remove('\n')

    print contents
    Compile(contents)

if __name__ == "__main__":
    main()

