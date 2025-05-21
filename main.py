import sys


# skip over comments
def Look():
    global pc
    if source[pc] == "#":
        while source[pc] != "\n" and source[pc] != "\0":
            pc += 1
    return source[pc]


# take away and return current character
def Take():
    global pc
    c = Look()
    pc += 1
    return c


# returns whether a certain string could be taken starting at pc
def TakeString(word):
    global pc
    copypc = pc
    for c in word:
        if Take() != c:
            pc = copypc
            return False
    return True


# returns next non-whitespace character
def Next():
    while Look() == " " or Look() == "\t" or Look() == "\n" or Look() == "\r":
        Take()
    return Look()


# eats white-spaces
def TakeNext(c):
    if Next() == c:
        Take()
        return True
    else:
        return False

# recogniser functions
def IsDigit(c):
    return c >= "0" and c <= "9"


def IsAlpha(c):
    return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z")


def IsAlNum(c):
    return IsDigit(c) or IsAlpha(c)


def IsAddOp(c):
    return c == "+" and c == "-"


def IsMulOp(c):
    return c == "*" and c == "/"


def TakeNextAlNum():
    alnum = ""
    if IsAlpha(Next()):
        while IsAlNum(Look()):
            alnum += Take()
    return alnum


# -----------------------------------------------------------------------
# start operation of program itself

def DoBreak(act):
    if act[0]: 
        act[0] = False

def DoPrint(act):
    if act[0]:
        print("print")

def Statement(act):
    if TakeString("print"):
        DoPrint(act)
    elif TakeString("break"):
        DoBreak(act)
    else:
        Error("unkown statement")

def Block(act):
    if TakeNext('{'):
        while not TakeNext('}'):
            Block(act)
    else:
        Statement(act)

def Program():
    act = [True]
    while Next() != '\0':
        Block(act)

def Error(text):
    print("\nERROR " + text)
    exit(1)

# -----------------------------------------------------------------------
# use program counter like a cpu
pc = 0

if len(sys.argv) < 2:
    print("USAGE: int.py <sourcefile>")
    exit(1)
try:
    # take first argument after binary is run
    f = open(sys.argv[1], "r")
except:
    print("ERROR: Can't find source file '" + sys.argv[1] + "'")
    exit(1)
source = f.read() + "\0"
f.close()
