#!/usr/bin/python

import sys
import re

tokens = {
    "number":       (0,r'\d+'),
    "rint":         (1,r'\$int'),
    "begin":        (2,r'\$begin'),
    "end":          (3,r'\$end'),
    "move":         (4,r'\$move'),
    "turn":         (5,r'\$turn'),
    "define":       (6,r'\$define'),
    "arg_right":    (7,r'right'),
    "arg_forward":  (8,r'forward'),
    "identifier":   (9,r'[a-zA-Z][a-zA-Z0-9_]*'),
    "oparenthesis": (10,r'\('),
    "cparenthesis": (11,r'\)'),
    "comma":        (12,r','),
    "equal":        (13,r':='),
    "plus":         (14,r'\+'),
    "minus":        (15,r'\-'),
    "comment":      (16,r'//.*'),
    "newline":      (17,r'\n'),
    "whitespace":   (18,r' '),
    "rstring":      (19,r'\$string'),
    "print":        (20,r'\$print'),
    "string":       (21,r'\".*\"')
}

sym_table = {"none": (0,"integer")}

OTHER_LEXEMA = 255
INSTRUCTION  = 0
ARGUMENT     = 1

error = 0
idx   = 0
llen  = 0
debug_mode = False

output = ""

def message(mtype,expected,received,description):
    print "{}. {} expected, {} received. {}".format(mtype,expected,received,description)

def get_token(lexema):
    global debug_mode
    ret = OTHER_LEXEMA
    for key in tokens:
        if re.match(tokens[key][1],lexema):
            ret = tokens[key][0]
            if debug_mode:
                print "{}\tis\t{}".format(lexema,key)
            break
    if ret == OTHER_LEXEMA:
        message("E","TOKEN",lexema,"Does not match any pattern.")
    return ret

def is_definition(token):
    ret = False
    if token == tokens["rint"][0] or token == tokens["rstring"][0]:
        ret = True
    return ret

def is_instruction(token):
    ret = False
    if token == tokens["move"][0] or token == tokens["turn"][0] or token == tokens["print"][0]:
        ret = True
    return ret

def is_command(token):
    ret = False
    if token == tokens["arg_right"][0] or tokens["arg_forward"][0] or token == tokens["arg_left"][0]:
        ret = True
    return ret

def generate_code(token,value):
    global output
    if token == tokens["print"][0]:
        output = output + "label "
    elif token == tokens["arg_right"][0]:
        output = output + "right "
    elif token == tokens["move"][0] or token == tokens["turn"][0]:
         previous_token = token
    elif token == tokens["arg_forward"][0]:
        output = output + "forward "
    elif token == tokens["number"][0]:
        output = output + value + " "
    elif token == tokens["string"][0]:
        tvalue = value.replace('\"','')
        output = output + tvalue + " "
    elif token == tokens["identifier"][0]:
        if sym_table.get(value, False):
            output = output + value + " "
    elif token == tokens["rint"][0] or token == tokens["rstring"][0]:
        output = output + "make "
    else:
        message("E",token,value,"No rule for this expression.")

def Variables(sequence):
    global idx
    global llen
    global output

    token = get_token(sequence[idx])
    while is_definition(token) and idx < llen:
         ttype = token
         generate_code(token,"")
         idx = idx + 1
         token = get_token(sequence[idx])
         variable = sequence[idx]
         if token == tokens["identifier"][0]:
             sym_table[variable] = (0, OTHER_LEXEMA)
             output = output + "\""
             generate_code(token,sequence[idx])
             idx = idx + 1
         else:
             message("E","identifier",sequence[idx],"Not a valid definition.")
         
         token = get_token(sequence[idx])
         if token == tokens["equal"][0]:
             idx = idx + 1
         else:
             message("E",":=",sequence[idx],"")

         token = get_token(sequence[idx])
         if token == tokens["number"][0]:
             if ttype == tokens["rint"][0]:
                 sym_table[variable] = (int(sequence[idx]), ttype)
                 generate_code(token,sequence[idx])
             else:
                 message("W","number",sequence[idx],"Wrong assignment.")
             idx = idx + 1
         elif token == tokens["string"][0]:
             if ttype == tokens["rstring"][0]:
                 sym_table[variable] = (sequence[idx], tokens["rstring"][0])
                 output = output + "\""
                 generate_code(token,sequence[idx])
             else:
                 message("W","string",sequence[idx],"Incorrect assignement.")
             idx = idx + 1
         else:
             print "Error. Not a value for {}".format(variable)
         output = output + '\n'
         token = get_token(sequence[idx])

def Defines(sequence):
    global idx
    global llen
    
    token = get_token(sequence[idx])
    while token == tokens["comment"][0] and idx < llen:
        idx = idx + 1
        token = get_token(sequence[idx])
    
    if token == tokens["define"][0] and idx < llen:
        idx = idx + 1
        Variables(sequence)
    else:
        error = 1
        message("E","$define",sequence[idx])

def Begin(sequence):
    global idx
    global llen
    token = get_token(sequence[idx])
    if token == tokens["begin"][0] and idx < llen:
        idx = idx + 1
    else:
        message("E","$begin",sequence[idx],"")

def Argument(sequence):
    global idx
    global llen
    token = get_token(sequence[idx])
    lexema = sequence[idx]
    if is_command(token): 
        generate_code(token,"")
        idx = idx + 1
    else:
        message("E","command",sequence[idx],"")

def Expression(sequence):
    global idx
    global llen
    global output

    token = get_token(sequence[idx])
    if token == tokens["number"][0] or token == tokens["identifier"][0] or token == tokens["string"][0]:
        if token == tokens["identifier"][0]:
            if sym_table.get(sequence[idx],False):
                if sym_table[sequence[idx]][1] == tokens["rstring"][0]:
                    output = output + ":"
        generate_code(token,sequence[idx])
        idx = idx + 1
    else:
        message("E","Number",sequence[idx],"")

def Commands(sequence):
    global idx
    global llen
    global output

    t1 = OTHER_LEXEMA
    token = get_token(sequence[idx])
    while is_instruction(token):
        arguments = 2
        t1 = token
        # generate coode according for the instruction
        generate_code(token,"")
        # check if it is one argument command
        if token == tokens["print"][0]:
            arguments = 1
        # increment index to check next token
        idx = idx + 1
        token = get_token(sequence[idx])
        if token == tokens["oparenthesis"][0]:
            idx = idx + 1
            # check move or turn commands
            if 1 < arguments:
                Argument(sequence)
                token = get_token(sequence[idx])
                # proces more arguments if needed
                if token == tokens["comma"][0]:
                    idx = idx + 1
                else:
                    message("E","\',\'",sequence[idx],"")
            # check the expression argument 
            Expression(sequence)
            token = get_token(sequence[idx])
            # check when parenthesis is closed
            if token == tokens["cparenthesis"][0]:
                idx = idx + 1
            else:
                message("E",")",sequence[idx],"")
        else:
            message("E","(",sequence[idx],"")
        output = output + '\n'
        # get a new token to continue processing more commands
        token = get_token(sequence[idx])

def End(sequence):
    global idx
    global llen
    token = get_token(sequence[idx])
    if token != tokens["end"][0]:
        message("E","$end",sequence[idx],"")

def Compile(sequence):
    global llen
    global idx
    llen = len(sequence)
    idx = 0
    Defines(sequence)
    Begin(sequence)
    Commands(sequence)
    End(sequence)

def main():
    global debug_mode
    global output

    contents = []
    with open(sys.argv[1], 'r') as f:
        contents = f.read()
        contents = re.split(r'(\".*\"|\n|[ ]|//.*|\d+|\$[a-zA-Z]+|[a-zA-Z][a-zA-Z0-9_]*|\(|\))',contents)
    
    while '' in contents: contents.remove('')
    while ' ' in contents: contents.remove(' ')
    while '\n' in contents: contents.remove('\n')

    if 3 <= len(sys.argv):
        if 1 == int(sys.argv[2]):
            debug_mode = True
            print "Debug Mode Activated"

    Compile(contents)
    print output

    if debug_mode:
        print contents
        print sym_table

if __name__ == "__main__":
    main()

