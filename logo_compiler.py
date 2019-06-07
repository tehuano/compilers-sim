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
    "arg_left":     (9,r'left',"left"),
    "arg_right":    (8,r'right',"right"),
    "arg_forward":  (10,r'forward',"forward"),
    "arg_backward": (11,r'backward',"back"),
    "arg_up":       (12,r'up',"up"),
    "arg_down":     (13,r'down',"down"),
    "arg_erase":    (14,r'erase',"erase"),
    "arg_paint":    (15,r'paint',"paint"),
    "oparenthesis": (19,r'\(',""),
    "cparenthesis": (20,r'\)',""),
    "comma":        (21,r',',""),
    "equal":        (22,r':=',""),
    "plus":         (23,r'\+',""),
    "minus":        (24,r'\-',""),
    "divide":       (25,r'\/',""),
    "multiply":     (26,r'\*',""),
    ">":            (27,r'\>',""),
    "<":            (28,r'\<',""),
    "lequal":       (53,r'==',""),
    "comment":      (29,r'//.*',""),
    "newline":      (30,r'\n',""),
    "whitespace":   (31,r' ',""),
    "rstring":      (32,r'\$string',"make"),
    "print":        (33,r'\$print',"label"),
    "string":       (34,r'\".*\"',""),
    "pencil":       (35,r'\$pencil',"pen"),
    "for":          (38,r'\$for',"repeat"),
    "setxy":        (39,r'\$setxy',"setxy"),
    "setx":         (40,r'\$setx',"setx"),
    "sety":         (41,r'\$sety',"sety"),
    "heading":      (42,r'\$heading',"setheading"),
    "arc":          (43,r'\$arc',"arc"),
    "home":         (44,r'\$home',"home"),
    "clean":        (45,r'\$clean',"clean"),
    "clear":        (46,r'\$clear',"clearscreen"),
    "bg":           (47,r'\$background',"setbackground"),
    "bye":          (48,r'\$bye',"bye"),
    "load":         (49,r'\$load',"load"),
    "pencolor":     (50,r'\$pencolor',"setpencolor"),
    "pensize":      (51,r'\$pensize',"setpensize"),
    "identifier":   (52,r'[a-zA-Z][a-zA-Z0-9_]*',"")
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

def needs_separator(token):
    ret = False
    if token == tokens["setxy"][0] or token == tokens["arc"][0]:
        ret = True
    return ret

def arg1_is_command(token):
    ret = False
    if token == tokens["move"][0] or token == tokens["turn"][0]:
        ret = True
    elif token == tokens["pencil"][0]:
        ret = True
    return ret

def arg1_is_expression(token):
    ret = False
    if token == tokens["print"][0] or token == tokens["if"][0]:
        ret = True
    elif token == tokens["setxy"][0] or token == tokens["heading"][0]:
        ret = True
    elif token == tokens["setx"][0] or token == tokens["sety"][0]:
        ret = True
    elif token == tokens["arc"][0] or token == tokens["bg"][0]:
        ret = True
    elif token == tokens["pencolor"][0] or token == tokens["pensize"][0]:
        ret = True
    elif token == tokens["load"][0] or token == tokens["for"][0]:
        ret = True
    return ret

def is_control(token):
    ret = False
    if token == tokens["if"][0] or token == tokens["for"][0]:
        ret = True
    return ret

def is_operator(token):
    ret = False
    if token == tokens["plus"][0] or token == tokens["minus"][0]:
        ret = True
    elif token == tokens["multiply"][0] or token == tokens["divide"][0]:
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
    elif token == tokens["for"][0] or token == tokens["pencil"][0]:
        ret = True
    elif token == tokens["setxy"][0] or token == tokens["setx"][0]:
        ret = True
    elif token == tokens["sety"][0] or token == tokens["heading"][0]:
        ret = True
    elif token == tokens["arc"][0] or token == tokens["home"][0]:
        ret = True
    elif token == tokens["clean"][0] or token == tokens["clear"][0]:
        ret = True
    elif token == tokens["load"][0] or token == tokens["bye"][0]:
        ret = True
    elif token == tokens["pencolor"][0] or token == tokens["pensize"][0]:
        ret = True
    elif token == tokens["bg"][0]:
        ret = True
    return ret

def is_command(token):
    ret = False
    if token == tokens["arg_right"][0] or token == tokens["arg_left"][0]:
        ret = True
    elif token == tokens["arg_forward"][0] or token == tokens["arg_backward"][0]:
        ret = True
    elif token == tokens["arg_down"][0] or token == tokens["arg_up"][0]:
        ret = True
    elif token == tokens["arg_erase"][0] or token == tokens["arg_paint"][0]:
        ret = True
    return ret

def number_of_arguments(token):
    ret = 2
    if token == tokens["print"][0] or token == tokens["if"][0]:
        ret = 1
    elif token == tokens["for"][0] or token == tokens["bg"][0]:
        ret = 1
    elif token == tokens["setx"][0] or token == tokens["sety"][0]:
        ret = 1
    elif token == tokens["heading"][0] or token == tokens["load"][0]:
        ret = 1
    elif token == tokens["pencil"][0] or token == tokens["pencolor"][0] or token == tokens["pensize"][0]:
        ret = 1
    elif token == tokens["home"][0] or token == tokens["clean"][0] or token == tokens["clear"][0] or token == tokens["bye"][0]:
        ret = 0
    return ret

def is_terminal(token):
    ret = False
    if token == tokens["number"][0] or token == tokens["identifier"][0] or token == tokens["string"][0]:
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
                output = output + tokens[keyt][2]
                if token != tokens["pencil"][0]:
                    output = output + ' '
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
        elif "Expression" == caller.function:
            if token == tokens["string"][0]:
                valuet = '\"' + valuet.replace('\"','')
        # assing the formated string or variable 
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
             message("W",variable,"value","Wrong value.")
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

def Command(sequence):
    global idx
    global llen
    token = get_token(sequence[idx])
    lexema = sequence[idx]
    if is_command(token):
        generate_code(token,"")
        idx = idx + 1
    else:
        message("E","command",lexema,"")

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
            idx = idx + 1
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
        t1 = token
        # generate code according for the instruction
        generate_code(token,"")
        # check if it is one argument command
        arguments = number_of_arguments(token)
        # increment index to check next token
        idx = idx + 1
        token = get_token(sequence[idx])
        if token == tokens["oparenthesis"][0]:
            idx = idx + 1
            if 1 <= arguments:
                if arg1_is_command(t1):
                    Command(sequence)
                elif arg1_is_expression(t1):
                    Expression(sequence)
                else:
                    message("E","Command or Expression",sequence[idx],"Not correct.")

            # proces more arguments if needed
            if 1 < arguments:
                token = get_token(sequence[idx])
                if token == tokens["comma"][0]:
                    idx = idx + 1
                    if needs_separator(t1):
                        output = output + ' '
                    Expression(sequence)
                else:
                    message("E","comma",sequence[idx],"")
            
            token = get_token(sequence[idx])
            # check when parenthesis is closed
            if token == tokens["cparenthesis"][0]:
                idx = idx + 1
            else:
                message("E",")",sequence[idx],"")
        else:
            message("E","(",sequence[idx],"")
        # if this is the body of an if sentence
        if is_control(t1):
            Begin(sequence)
            if False == error:
                output = output + ' [\n'
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

