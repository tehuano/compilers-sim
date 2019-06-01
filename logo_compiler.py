#!/usr/bin/python

import sys
import re

tdigit     = '\d+'
trvariable = '\$var'
trbegin    = '\$begin'
trend      = '\$end'
trmove     = '\$move'
trturn     = '\$turn'
trdefine   = '\$define'
taright    = 'right'
taforward  = 'forward'

tidentifier   = '[a-zA-Z]+'
toparenthesis = '\('
tcparenthesis = '\)'
tccomma   = ','
tcequal  = ':='
tcplus    = '\+'
tcminus   = '\-'
tcomment = '//.*' 
tnewline    = '\n' 
twhitespace = ' ' 

NUMBER       = 0
VARIABLE     = 1
BEGIN        = 2
END          = 3
OPARENTHESIS = 4
CPARENTHESIS = 5
COMMA        = 6
COMMENT      = 7
NEWLINE      = 8
WHITESPACE   = 9
MOVE         = 10
DEFINE       = 11
IDENTIFIER   = 12
EQUAL        = 13
TURN         = 14
ARGRIGHT     = 15
ARGFORWARD   = 16

NOTOKEN = 255

error = 0
idx   = 0
llen  = 0

def print_lexema(ret,lexema):
    if ret == NUMBER:
        print("{}\tis\tNUMBER".format(lexema))
    elif ret == VARIABLE:
        print("{}\tis\tVARIABLE".format(lexema))
    elif ret == BEGIN:
        print("{}\tis\tBEGIN".format(lexema))
    elif ret == END:
        print("{}\tis\tEND".format(lexema))
    elif ret == OPARENTHESIS:
        print("{}\tis\tOPARENTHESIS".format(lexema))
    elif ret == CPARENTHESIS:
        print("{}\tis\tCPARENTHESIS".format(lexema))
    elif ret == COMMA:
        print("{}\tis\tCOMMA".format(lexema))
    elif ret == COMMENT:
        print("{}\tis\tCOMMENT".format(lexema))
    elif ret == NEWLINE:
        print("{}\tis\tNEWLINE".format("nl"))
    elif ret == NOTOKEN:
        print("{}\tis\tNOTOKEN".format(lexema))
    elif ret == WHITESPACE:
        print("{}\tis\tWHITESPACE".format(lexema))
    elif ret == DEFINE:
        print("{}\tis\tDEFINE".format(lexema))
    elif ret == MOVE:
        print("{}\tis\tMOVE".format(lexema))
    elif ret == EQUAL:
        print("{}\tis\tEQUAL".format(lexema))
    elif ret == IDENTIFIER:
        print("{}\tis\tIDENTIFIER".format(lexema))
    elif ret == TURN:
        print("{}\tis\tTURN".format(lexema))
    elif ret == ARGRIGHT:
        print("{}\tis\tARIGHT".format(lexema))
    elif ret == ARGFORWARD:
        print("{}\tis\tAFORWARD".format(lexema))
    elif ret == TURN:
        print("{}\tis\tTURN".format(lexema))
    else:
        print("{}\tis\tOTHER".format(lexema))

def get_token(lexema):
    ret = NOTOKEN
    if re.match(tdigit, lexema):
        ret = NUMBER
    elif re.match(trvariable, lexema):
        ret = VARIABLE
    elif re.match(trbegin, lexema):
        ret = BEGIN
    elif re.match(trend, lexema):
        ret = END
    elif re.match(toparenthesis, lexema):
        ret = OPARENTHESIS
    elif re.match(tcparenthesis, lexema):
        ret = CPARENTHESIS
    elif re.match(tccomma, lexema):
        ret = COMMA
    elif re.match(tcequal, lexema):
        ret = EQUAL
    elif re.match(tcomment, lexema):
        ret = COMMENT
    elif re.match(tnewline, lexema):
        ret = NEWLINE
    elif re.match(twhitespace, lexema):
        ret = WHITESPACE
    elif re.match(trdefine, lexema):
        ret = DEFINE
    elif re.match(trmove, lexema):
        ret = MOVE
    elif re.match(trturn, lexema):
        ret = TURN
    elif re.match(taforward, lexema):
        ret = ARGFORWARD
    elif re.match(taright, lexema):
        ret = ARGRIGHT
    elif re.match(tidentifier, lexema):
        ret = IDENTIFIER

    return ret


def Variables(sequence):
    global idx
    global llen

    token = get_token(sequence[idx])
    print_lexema(token,sequence[idx])
    while token == VARIABLE and idx < llen:
         idx = idx + 1
         token = get_token(sequence[idx])
         print_lexema(token,sequence[idx])
         if token == IDENTIFIER:
             idx = idx + 1
         else:
             print "Error !!"
         
         token = get_token(sequence[idx])
         print_lexema(token,sequence[idx])
         if token == EQUAL:
             idx = idx + 1
         else:
             print "Error !!"

         token = get_token(sequence[idx])
         if token == NUMBER:
             idx = idx + 1
         else:
             print "Error !!"

def Defines(sequence):
    global idx
    global llen
    
    token = get_token(sequence[idx])
    print_lexema(token,sequence[idx])
    while token == COMMENT and idx < llen:
        idx = idx + 1
        token = get_token(sequence[idx])
        print_lexema(token,sequence[idx])
    
    if token == DEFINE and idx < llen:
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
    if token == BEGIN and idx < llen:
        idx = idx + 1
    else:
        print "Error !!"

def Argument(sequence):
    global idx
    global llen
    token = get_token(sequence[idx])
    print_lexema(token,sequence[idx])
    if token == ARGRIGHT or ARGFORWARD:
        idx = idx + 1
    else:
        print "Error !!"

def Expression(sequence):
    global idx
    global llen
    token = get_token(sequence[idx])
    print_lexema(token,sequence[idx])
    if token == NUMBER:
        idx = idx + 1
    else:
        print "{} Error !!".format(sequence[idx])

def Behaviour(sequence):
    global idx
    global llen
    token = get_token(sequence[idx])
    print_lexema(token,sequence[idx])
    while token == MOVE or token == TURN:
        idx = idx + 1
        token = get_token(sequence[idx])
        print_lexema(token,sequence[idx])
        if token == OPARENTHESIS:
            idx = idx + 1
            Argument(sequence)
            token = get_token(sequence[idx])
            print_lexema(token,sequence[idx])
            if token == COMMA:
                idx = idx + 1
                Expression(sequence)
                token = get_token(sequence[idx])
                print_lexema(token,sequence[idx])
                if token == CPARENTHESIS:
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
    if token != END:
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

