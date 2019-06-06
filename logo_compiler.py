#!/usr/bin/python

import sys
import re
import inspect

tokens = {
    "number":       (0,r'\d+',""),
    "rint":         (1,r'\$int',"make"),
    "begin":        (2,r'\$begin',""),
    "end":          (3,r'\$end',""),
    "move":         (4,r'\$move',""),
    "turn":         (5,r'\$turn',""),
    "define":       (6,r'\$define',""),
    "if":           (7,r'\$if',"if"),
    "arg_right":    (8,r'right',"right"),
    "arg_left":     (9,r'left',"left"),
    "arg_forward":  (10,r'forward',"forward"),
    "arg_backward": (11,r'backward',"backward"),
    "identifier":   (12,r'[a-zA-Z][a-zA-Z0-9_]*',""),
    "oparenthesis": (13,r'\(',""),
    "cparenthesis": (14,r'\)',""),
    "comma":        (15,r',',""),
    "equal":        (16,r':=',""),
    "plus":         (17,r'\+',""),
    "minus":        (19,r'\-',""),
    "divide":       (20,r'\/',""),
    "multiply":     (21,r'\*',""),
    ">":            (22,r'\>',""),
    "<":            (23,r'\<',""),
    "comment":      (24,r'//.*',""),
    "newline":      (25,r'\n',""),
    "whitespace":   (26,r' ',""),
    "rstring":      (27,r'\$string',"make"),
    "print":        (28,r'\$print',"label"),
    "string":       (29,r'\".*\"',"")
}

sym_table = {"none": (0,"integer")}

OTHER_LEXEMA = 255
INSTRUCTION  = 0
ARGUMENT     = 1

error = False
idx   = 0
llen  = 0
debug_mode = False

output = ""
spaces = 0
previous_token = OTHER_LEXEMA

def message(mtype,expected,received,description):
    global error
    debug_info = ""
    if debug_mode:
        for st in inspect.stack():
            caller = inspect.getframeinfo(st[0])
            debug_info = debug_info + "{}:{} At {} ".format(caller.filename,caller.lineno,caller.function)
    if mtype == "E":
        error = True
    print "{}. {} expected, {} received. {} {}".format(mtype,expected,received,description,debug_info)

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

def is_operator(token):
    ret = False
    if token == tokens["plus"][0] or token == tokens["minus"][0]:
        ret = True
    return ret

def is_comparator(token):
    ret = False
    if token == tokens[">"][0] or token == tokens["<"][0]:
        ret = True
    return ret

def is_definition(token):
    ret = False
    if token == tokens["rint"][0] or token == tokens["rstring"][0]:
        ret = True
    return ret

def is_statement(token):
    ret = False
    if token == tokens["move"][0] or token == tokens["turn"][0]:
        ret = True
    elif token == tokens["print"][0] or token == tokens["if"][0]:
        ret = True
    return ret

def is_command(token):
    ret = False
    if token == tokens["arg_right"][0] or token == tokens["arg_left"][0]:
        ret = True
    elif token == tokens["arg_forward"][0] or token == tokens["arg_backward"][0]:
        ret = True
    return ret

def is_one_argument(token):
    ret = False
    if token == tokens["print"][0] or token == tokens["if"][0]:
        ret = True
    return ret

def is_terminal(token):
    ret = False
    if token == tokens["number"][0] or token == tokens["identifier"][0]:
        ret = True
    elif token == tokens["string"][0]:
        ret = True
    return ret

def print_spaces():
    global spaces
    global output
    # write identation
    id = ''
    for x in range(spaces):
        id = id + ' '
        output = output + id

def generate_code(token,value):
    global output
    global previous_token
    global error

    if is_statement(token):
        print_spaces()
    if not is_terminal(token):
        found = False
        keyt = ""
        for key in tokens:
            if token == tokens[key][0]:
                found = True
                keyt = key
                break
        if found:
            if token == tokens["move"][0] or token == tokens["turn"][0]:
                previous_token = token
            if tokens[keyt][2]:
                output = output + tokens[keyt][2] + ' '
        else:
            error = True
            message("E",token,value,"No rule for this expression gen_code.")
    else:
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        valuet = value
        if "Variables" == caller.function:
            if token == tokens["string"][0] or token == tokens["identifier"][0]:
                if token == tokens["string"][0]:
                    valuet = valuet.replace('\"','')
                valuet = '\"' + valuet
        output = output + valuet
        if "Variables" == caller.function:
            output = output + ' '

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
    # process a definition
    if token == tokens["define"][0] and idx < llen:
        idx = idx + 1
        Variables(sequence)
    else:
        error = True
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

def ArithmeticExpression(sequence):
    global idx
    global llen
    global output

    token = get_token(sequence[idx])
    if is_terminal(token):
        generate_code(token,sequence[idx])
        idx = idx + 1
        token = get_token(sequence[idx])
        if is_operator(token):
            output = output + sequence[idx]
            idx = idx + 1
            ArithmeticExpression(sequence)
        elif is_comparator(token):
            output = output + sequence[idx]
            idx = idx +1
            LogicalExpression(sequence)
    else:
        message("E","Expression",sequence[idx],"")

def LogicalExpression(sequence):
    global idx
    global llen
    global output

    token = get_token(sequence[idx])
    if is_terminal(token):
        generate_code(token,sequence[idx])
        idx = idx + 1
        token = get_token(sequence[idx])
        if is_operator(token):
            output = output + sequence[idx]
            idx = idx + 1
            ArithmeticExpression(sequence)
        elif is_comparator(token):
            output = output + sequence[idx]
            idx = idx +1
            LogicalExpression(sequence)
    else:
        message("E","Expression",sequence[idx],"")

def Expression(sequence):
    global idx
    global llen
    global output

    token = get_token(sequence[idx])
    if is_terminal(token):
        generate_code(token,sequence[idx])
        idx = idx + 1
        token = get_token(sequence[idx])
        if is_operator(token):
            output = output + sequence[idx]
            idx = idx + 1
            ArithmeticExpression(sequence)
        elif is_comparator(token):
            output = output + sequence[idx]
            idx = idx +1
            LogicalExpression(sequence)
    else:
        message("E","Expression",sequence[idx],"")

def Statements(sequence):
    global idx
    global llen
    global output
    global spaces

    t1 = OTHER_LEXEMA
    token = get_token(sequence[idx])
    while is_statement(token):
        arguments = 2
        t1 = token
        # generate code according for the instruction
        generate_code(token,"")
        # check if it is one argument command
        if is_one_argument(token):
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
        # if this is the body of an if sentence
        if t1 == tokens["if"][0]:
            Begin(sequence)
            if False == error:
                print_spaces()
                output = output + '[\n'
                spaces = spaces + 1
            Statements(sequence)
            End(sequence)
            if False == error:
                spaces = spaces - 1
                print_spaces()
                output = output + ']'
        # get a new token to continue processing more commands
        token = get_token(sequence[idx])
        output = output + '\n'

def End(sequence):
    global idx
    global llen
    token = get_token(sequence[idx])
    if token == tokens["end"][0]:
        idx = idx + 1
    else:
        message("E","$end",sequence[idx],"")

def Compile(sequence):
    global llen
    global idx
    llen = len(sequence)
    idx = 0
    Defines(sequence)
    Begin(sequence)
    Statements(sequence)
    End(sequence)

def main():
    global debug_mode
    global output

    contents = []
    with open(sys.argv[1], 'r') as f:
        contents = f.read()
        contents = re.split(r'(\".*\"|\n|[ ]|//.*|\d+|\$[a-zA-Z]+|[a-zA-Z][a-zA-Z0-9_]*|\(|\)|<|>|\/|\*)',contents)
    
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

