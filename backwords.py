#!/usr/bin/env python3

import sys, argparse

DIGITS = '0123456789ABCDEF'

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('-debug', action='store_true')
args = parser.parse_args()

if args.debug:
    print('debug ON')

with open(args.file, 'r') as f:
    program = f.read() 

ip = 0                # instruction pointer 
stack = bytearray([]) # data stack 

# memory
tape = bytearray([0 for x in range(256)]) 
page = 0

def pop ():
    return stack.pop()

def push (x):
    stack.append(int(x) % 256)

def tape_expand (index_required):
    # Virtually infinite memory
    while len(tape) < index_required:
        tape += bytearray([0 for x in range(256)])

def execute (x):
    global tape, stack, ip, page, running 
    if ':' == x:
        # dup 
        if stack:
            push(stack[-1])
    elif x in DIGITS:
        # Numbers, base 16
        top = stack[-1]
        top *= 16
        top += DIGITS.index(x)
        stack[-1] = top % 256
    elif '+' == x:
        # add
        push(pop() + pop())
    elif '-' == x:
        # subtract
        push(pop() - pop())
    elif '*' == x:
        # multiply
        push(pop() * pop())
    elif '/' == x:
        # divide
        push(pop() // pop())
    elif '%' == x:
        # mod
        push(pop() % pop())
    elif '`' == x:
        # Bitwise not the TOS
        push(~pop())
    elif '&' == x:
        # Bitwise and
        push(pop() & pop())
    elif '|' == x:
        # Bitwise or
        push(pop() | pop())
    elif ',' == x:
        # emit
        val = pop()
        sys.stdout.write(chr(val))
    elif '?' == x:
        # input
        c = sys.stdin.read(1)
        push(ord(c))
    elif ';' == x:
        # halt the outer infinite loop
        running = False
    elif '\\' == x:
        # Loop back
        ip = -1 # it will be incremented to zero in an outer loop
    elif '_' == x:
        # Drop the top of the stack
        pop()
    elif '#' == x:
        # Used to start a number
        push(0)
    elif "'" == x:
        # literal char
        ip += 1
        push(ord(program[ip]))
    elif '=' == x:
        # equal
        a, b = pop(), pop()
        c = a == b
        push(255 if c else 0)
    elif '>' == x:
        top, top2 = pop(), pop()
        c = top2 > top
        push(255 if c else 0)
    elif '<' == x:
        top, top2 = pop(), pop()
        c = top2 < top
        push(255 if c else 0)
    elif '.' == x:
        # eval
        execute(chr(pop()))
    elif '^' == x:
        # branch forward
        ip += pop()
    elif 'v' == x:
        # branch backwards
        ip -= pop() + 1
    elif 'n' == x:
        # Conditional (is not zero)
        do_skip = pop() == 0
        if do_skip:
            ip += 1
    elif 'z' == x:
        # Inverted conditional
        do_skip = pop() != 0
        if do_skip:
            ip += 1
    elif 'u' == x.lower():
        # Clear the stack
        stack = []
    elif 's' == x.lower():
        # Swap 2 numbers on the stack
        a, b = pop(), pop()
        push(a)
        push(b)
    elif '{' == x:
        # Previous memory page
        page -= 1
    elif '}' == x:
        # Next memory page
        page += 1
    elif '@' == x:
        # Tape fetch
        index = page * 256 + pop()
        if index not in range(len(tape)):
            tape_expand()
        push(tape[index])
    elif '!' == x:
        # Tape store
        index = pop()
        value = pop()
        index += page * 256
        if index not in range(len(tape)):
            tape_expand()
        tape[index] = value 
    elif 'i' == x:
        # Get the instruction [i] characters before the current ip
        i = ip - pop() 
        push(ord(program[i]))
    elif 'I' == x:
        # Get the instruction [I] character after the current ip
        i = ip + pop()
        push(ord(program[i]))
    elif '$' == x:
        # Get the stack size
        push(len(stack))
    elif 'g' == x.lower():
        # Print debug info
        print('stack [%s]' %(','.join(str(x) for x in stack)))
    elif 'k' == x.lower():
        # Debug "breakpoint"
        input('pause...')
    elif '"' == x:
        # Read a string
        char = ''
        while char != '"':
            if char:
                if '\\' == char:
                    escape = True
                    ip += 1
                    char = program[ip]
                push(ord(char))
            ip += 1
            char = program[ip]
    else:
        # Ignore other characters
        pass
        
try:
    running = True
    while running: 
        # The program counter automatically loops back around,
        # and the empty program will run an infinite loop 
        if ip >= len(program):
            ip = 0
            continue
        x = program[ip]  
        execute(x)
        ip += 1
except Exception as e:
    if args.debug:
        raise e
    sys.exit(-1)
