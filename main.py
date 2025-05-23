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


# and create a boolean factor
def BooleanFactor(act):
    inv = TakeNext("!")
    e = Expression(act)
    b = e[1]
    Next()
    if e[0] == "i":
        if TakeString("=="):
            b = b == MathExpression(act)
        elif TakeString("!="):
            b = b != MathExpression(act)
        elif TakeString("<="):
            b = b <= MathExpression(act)
        elif TakeString("<"):
            b = b < MathExpression(act)
        elif TakeString(">="):
            b = b >= MathExpression(act)
        elif TakeString(">"):
            b = b > MathExpression(act)
    else:
        if TakeString("=="):
            b = b == StringExpression(act)
        elif TakeString("!="):
            b = b != StringExpression(act)
        else:
            b = b != ""
    # always return false if inactive
    return act[0] and (b != inv)


# allow for boolean terms
def BooleanTerm(act):
    b = BooleanFactor(act)
    while TakeNext("&"):
        b = b & BooleanFactor(act)
    return b


# boolean expressions
def BooleanExpression(act):
    b = BooleanExpression(act)
    while TakeNext("|"):
        b = b | BooleanTerm(act)
    return b


# define a math factor
def MathFactor(act):
    m = 0
    # allow for round brackets surrounding a maths expression
    if TakeNext("("):
        m = MathExpression(act)
        if not TakeNext(")"):
            Error("missing ')'")
    # check for just a raw number
    elif IsDigit(Next()):
        while IsDigit(Look()):
            m = 10 * m + ord(Take()) - ord("0")
    # allow for the value of a string
    elif TakeString("val("):
        s = String(act)
        if act[0] and s.isdigit():
            m = int(s)
        if not TakeNext(")"):
            Error("missing ')'")
    # aand value of a variable
    else:
        ident = TakeNextAlNum()
        if ident not in variable or variable[ident][0] != "i":
            Error("unkown variable")
        elif act[0]:
            m = variable[ident][1]
    return m


# Math Term is a factor followed by * or / followed by another term
def MathTerm(act):
    m = MathFactor(act)
    while IsMulOp(Next()):
        c = Take()
        m2 = MathFactor(act)
        if c == "*":
            m = m * m2
        else:
            m = m / m2
    return m


# implement math expressions
def MathExpression(act):
    c = Next()
    if IsAddOp(c):
        c = Take()
    m = MathTerm(act)
    if c == "-":
        m = -m
    while IsAddOp(Next()):
        c = Take()
        m2 = MathTerm(act)
        if c == "+":
            # addition
            m = m + m2
        else:
            # subtraction
            m = m - m2
    return m


# actually implement strings
def String(act):
    s = ""
    # literal strings
    if TakeNext('"') or TakeNext("'"):
        while not TakeString('"') or not TakeString("'"):
            if Look() == "\0":
                Error("unexpected EOF")
            if TakeString("\\n"):
                s += "\n"
            else:
                s += Take()
    # evaluations of maths expressions
    elif TakeString("str("):
        s = str(MathExpression(act))
        if not TakeNext(")"):
            Error("missing ')'")
    # content of a user input
    elif TakeString("input()"):
        if act[0]:
            s = input()
    # content of a variable
    else:
        ident = TakeNextAlNum()
        if ident in variable and variable[ident][0] == "s":
            s = variable[ident][1]
        else:
            Error("not a string")
    return s


# define string expressions
def StringExpression(act):
    s = String(act)
    while TakeNext("+"):
        s += String(act)
    return s


def Expression(act):
    global pc
    copypc = pc
    ident = TakeNextAlNum()
    pc = copypc
    if (
        Next() == '"'
        or ident == "str"
        or ident == "input"
        or (ident in variable and variable[ident][0] == "s")
    ):
        return ("s", StringExpression(act))
    else:
        return ("i", MathExpression(act))


# run functions
def DoGoSub(act):
    global pc
    ident = TakeNextAlNum()
    if ident not in variable or variable[ident][0] != "p":
        Error("unknown subroutine")
    # execute block as subroutine
    ret = pc
    pc = variable[ident][1]
    Block(act)
    pc = ret


# define subroutines/functions
def DoSubDef():
    global pc
    ident = TakeNextAlNum()
    if ident == "":
        Error("missing subroutine identifier")
    variable[ident] = ("p", pc)
    Block([False])


# variable assignments
def DoAssign(act):
    ident = TakeNextAlNum()
    if not TakeNext("=") or ident == "":
        Error("unknown statement")
    e = Expression(act)
    if act[0] or ident not in variable:
        variable[ident] = e


# print statements
def DoPrint(act):
    while True:
        e = Expression(act)
        if act[0]:
            print(e[1], end="")
        if not TakeNext(","):
            return


def Statement(act):
    if TakeString("OUTPUT"):
        DoPrint(act)
    elif TakeString("gosub"):
        DoGoSub(act)
    elif TakeString("SUBROUTINE"):
        DoSubDef()
    else:
        DoAssign(act)


def Block(act):
    if TakeNext("{"):
        while not TakeNext("}"):
            Block(act)
    else:
        Statement(act)


def Program():
    act = [True]
    while Next() != "\0":
        Block(act)


def Error(text):
    s = source[:pc].rfind("\n") + 1
    e = source.find("\n", pc)
    print(
        "\nERROR "
        + text
        + " in line "
        + str(source[:pc].count("\n") + 1)
        + ": '"
        + source[s:pc]
        + "_"
        + source[pc:e]
    )
    exit(1)


# -----------------------------------------------------------------------
# use program counter like a cpu
pc = 0
# initialise dictionary for variables
variable = {}

if len(sys.argv) < 2:
    print("USAGE: int.py <sourcefile>")
    exit(1)
try:
    # take first argument after binary is run
    f = open(sys.argv[1], "r")
except:  # noqa: E722
    print("ERROR: Can't find source file '" + sys.argv[1] + "'")
    exit(1)
source = f.read() + "\0"
f.close()

Program()