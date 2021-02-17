#!/usr/bin/env python3

import sys
from getch import getch

V_TRUE = 255
V_FALSE = 0
DIGITS = '0123456789ABCDEF'
debug = False
debug2 = False

if len(sys.argv) != 2:
    print('Usage:')
    print(sys.argv[0], '[filename]')
    sys.exit(-1)

filename = sys.argv[1]
with open(filename, 'r') as f:
    program = f.read() 

ip = 0 # instruction pointer 
stack = bytearray([])
tape = bytearray([0 for x in range(256)])
memory_page = 0

def pop ():
    return stack.pop()

def push (x):
    stack.append(int(x) % 256)

def tape_expand (index_required):
    # Virtually infinite memory
    while len(tape) < index_required:
        tape += bytearray([0 for x in range(256)])

def execute (x):
    global tape, stack, ip, memory_page

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
        push(pop() / pop())
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
        char = chr(val)
        print(end=char)
    elif '?' == x:
        # input
        c = getch() 
        push(ord(c))
        if c == b'\x03':
            # ^C received
            raise KeyboardInterrupt()
    elif ';' == x:
        # halt the outer infinite loop
        raise SystemExit()
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
        push(V_TRUE if c else V_FALSE)
    elif '>' == x:
        top, top2 = pop(), pop()
        c = top2 > top
        push(V_TRUE if c else V_FALSE)
    elif '<' == x:
        top, top2 = pop(), pop()
        c = top2 < top
        push(V_TRUE if c else V_FALSE)
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
        # conditional
        do_skip = pop() == V_FALSE
        if do_skip:
            ip += 1
    elif 'z' == x:
        # inverted conditional
        do_skip = pop() != V_FALSE
        if do_skip:
            ip += 1
    elif 'u' == x.lower():
        # Clear the stack
        stack = []
    elif 's' == x.lower():
        # swap 
        a, b = pop(), pop()
        push(a)
        push(b)
    elif '{' == x:
        memory_page -= 1
    elif '}' == x:
        memory_page += 1
    elif '@' == x:
        # Tape fetch
        index = memory_page * 256 + pop()
        if index not in range(len(tape)):
            tape_expand()
        push(tape[index])
    elif '!' == x:
        # Tape store
        index, value = pop(), pop()
        index += memory_page * 256
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
        print('debug: [%s]' %(','.join(str(x) for x in stack)))
    elif 'k' == x.lower():
        # Debug "breakpoint"
        input('pause:')
    elif '"' == x:
        # Read a string
        # TODO: add escape codes
        char = ''
        while char != '"':
            if char:
                push(ord(char))
            ip += 1
            char = program[ip]
    else:
        # Ignore characters that aren't assigned meaning
        pass
        
exception = False
ex = None
try:
    while True: 
        if debug2:
            print('ip:', ip)
            print('stack:', stack)
            print('program[ip]:', program[ip])
            print('-------------------------')
            input('{') 
        # The program counter automatically loops back around
        if ip >= len(program):
            ip = 0
            continue # This continue makes the empty program run an infinite loop 
        x = program[ip]  
        execute(x)
        ip += 1
except Exception as e:
    exception = True
    ex = e
finally:
    if debug:
        print()
        if exception: 
            print('----- exception -----')
        else:
            print('----- success!! -----')
        print('ip:', ip)
        print('stack:', stack)
        print('program[ip]:', program[ip])
        print('-------------------------')
        if exception:
            raise ex

