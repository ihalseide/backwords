#!/usr/bin/env python3

# Virtual Machine:
# Parameter Stack
stack = []
# Return Stack
returns = []
# Memory space
memory = []
# Instruction Pointer
ip = None

# Push to the Parameter Stack
def pop ():
    return stack.pop(-1)

# Pop from the Return Stack
def rpop ():
    return returns.pop(-1)

# Push to the Parameter Stack
def push (x):
    stack.append(x)

# Push to the Return Stack
def rpush (x):
    returns.append(x)

# "To R" >R, pops the Parameter Stack and pushes it to the Return Stack
def tor ():
    rpush(pop())

# "R From" R>, pops the Return Stack and pushes it to the Parameter Stack
def fromr ():
    push(rpop()) 

# Word to swap the top two cells on the stack
def swap () :
    top = pop()
    next_ = pop()
    push(top)
    push(next_)

# Word to duplicate/re-push the top of the stack
def dup ():
    push(stack[-1])

# Word to store a Cell value at an address
def store ():
    addr = pop()
    memory[addr] = pop()

# Word to fetch a byte value at an address
def cfetch ():
    push(memory[pop()])

# Word to perform addition
def add ():
    push(pop() + pop())

# Perform multiplication
def mul ():
    push(pop() * pop())

# Word to perform bitwise and
def nand ():
    push(!(pop() & pop()))

# Word to branch the instruction pointer relatively based on the top of the stack
def branch ():
    ip += pop()

# Word to skip the next instruction if the top of the stack is True (1)
def skip ():
    if pop():
        ip += 1

# Word to get a character from input
def query ():
    push((cell) getchar())

# Word to print a character
def dot ():
    putchar((char) pop())

# Word to push the next cell in the program to the stack
def lit ():
    push(get(ip + 1))
    ip += 1

# Word to exit the direct threaded code for a word
def exit_ ():
    ip = rpop()

def main ():
    program = [lit, ord('!'), dot]

main()
