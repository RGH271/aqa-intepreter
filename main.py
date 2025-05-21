import sys


# skip over comments
def Look():
    global pc
    if source[pc] == "#":
        while source[pc] != "\n" and source[pc] != "\0":
            pc += 1
    return source[pc]


#take away and return current character
def Take():
    global pc
    c = Look()
    pc += 1
    return c




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
