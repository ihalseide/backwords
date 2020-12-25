#!/usr/bin/env python3

class _Getch:
    '''Gets a single character from standard input. Does not echo to the
screen.'''
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
getch = _Getch()

# Virtual Machine:
class VM:
    # Parameter Stack
    stack = []
    # Return Stack
    returns = []
    # Memory space
    memory = []
    # Instruction Pointer
    ip = None
    # Word dictionary list
    dictionary = []
    # VM and Compiler state
    state = 'reset'
    is_compiling = False

    def __init__ (self):
        self.dictionary = [
            ('halt', self.halt),
            ('dup', self.dup),
            ('>R', self.tor),
            ('R>', self.fromr),
            ('swap', self.swap),
            ('drop', self.pop),
            ('!', self.store),
            ('@', self.fetch),
            ('+', self.add),
            ('-', self.sub),
            ('*', self.mul),
            ('&', self.and_),
            ('|', self.or_),
            ('branch', self.branch),
            ('skip', self.skip),
            ('?', self.query),
            ('.', self.dot),
            ('lit', self.lit),
            ('enter', self.enter),
            ('exit', self.exit)
        ]

    def halt (self):
        self.state = 'stopped'

    def next (self):
        if not self.state == 'stopped':
            t = self.memory[self.ip]
            self.do_primitive(t)
            self.ip += 1

    def is_primitive (self, token):
        return 0 <= token < len(self.dictionary)

    def do_primitive (self, token):
        code = self.dictionary[token][1]
        code()

    def primitive (self, name):
        names = [x[0] for x in self.dictionary]
        return names.index(name)

    def enter (self):
        # Get the next code/token
        token = self.memory[self.ip]
        self.ip += 1
        if self.is_primitive(token):
            # Execute primitive at token index
            self.do_primitive(token)
        else:
            # Jump to address in token
            self.rpush(self.ip)
            self.ip = token

    # Word to exit the direct threaded code for a word
    def exit (self):
        self.ip = self.rpop()

    def find (self, word):
        for i, x in enumerate(reversed(self.dictionary)):
            if x[0] == word:
                return i
        return None

    def sub (self):
        self.push(self.pop() - self.pop())
        
    # Push to the Parameter Stack
    def pop (self):
        return self.stack.pop(-1)

    # Pop from the Return Stack
    def rpop (self):
        return self.returns.pop(-1)

    # Push to the Parameter Stack
    def push (self, x):
        self.stack.append(x)

    # Push to the Return Stack
    def rpush (self, x):
        self.returns.append(x)

    # "To R" >R, pops the Parameter Stack and pushes it to the Return Stack
    def tor (self):
        self.rpush(self.pop())

    # "R From" R>, pops the Return Stack and pushes it to the Parameter Stack
    def fromr (self):
        self.push(self.rpop()) 

    # Word to swap the top two cells on the stack
    def swap (self) :
        top = self.pop()
        next_ = self.pop()
        self.push(top)
        self.push(self.next_)

    # Word to duplicate/re-push the top of the stack
    def dup (self):
        self.push(self.stack[-1])

    # Word to store a Cell value at an address
    def store ():
        addr = self.pop()
        self.memory[addr] = self.pop()

    # Word to fetch a byte value at an address
    def fetch ():
        push(memory[pop()])

    # Word to perform addition
    def add ():
        self.push(self.pop() + self.pop())

    # Perform multiplication
    def mul ():
        self.push(self.pop() * self.pop())

    # Word to perform bitwise and
    def and_ (self):
        self.push(self.pop() & self.pop())

    def or_ (self):
        self.push(self.pop() | self.pop())

    # Word to branch the instruction pointer relatively based on the top of the stack
    def branch (self):
        self.ip += self.pop()

    # Word to skip the next instruction if the top of the stack is True (1)
    def skip (self):
        if self.pop():
            self.ip += 1

    # Word to get a character from input
    def query (self):
        self.push(ord(getch()))

    # Word to print a character
    def dot (self):
        print(end=chr(self.pop()))

    # Word to push the next cell in the program to the stack
    def lit (self):
        self.push(get(ip + 1))
        self.ip += 1

