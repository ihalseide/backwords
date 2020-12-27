#!/usr/bin/env python3

from char_io import getch, putch
from iterable import iterable

class Word:
    def __init__ (self, function, immediate=False, hidden=False):
        self.function = function
        self.immediate = immediate
        self.hidden = hidden

def norm_word (x):
    if iterable(x):
        return Word(*x)
    else:
        return Word(x)

def norm_dict (dictionary):
    return {name: norm_word(w) for name, w in dictionary.items()}

# Virtual Machine:
class VM:

    def __init__ (self):
        # Parameter Stack
        self.stack = []
        # Return Stack
        self.rstack = []
        # Memory array ( * 1024 is kilobytes )
        self.memory = [0 for _ in range(10 * 1024)]
        # Virtual Instruction Pointer
        self.ip = 0
        # Compile mode or Interpret mode flag
        self.compiling = False
        # Word dictionary
        self.dictionary = self.init_dict()

    def init_dict (self):
        push = self.push
        pop = self.pop
        return norm_dict({
            'dup': lambda: push(self.stack[-1]),
            'drop': lambda: pop(),
            'swap': lambda: self.swap(),
            '@': lambda: push(self.fetch(pop())),
            '!': lambda: self.store(pop(), pop()),
            '+': lambda: push(pop() + pop()),
            '1+': lambda: push(+1 + pop()),
            '-': lambda: push(pop() - pop()),
            '1-': lambda: push(-1 + pop()),
            '*': lambda: push(pop() * pop()),
            '**': lambda: push(pop() ** pop()),
            '/': lambda: push(pop() / pop()),
            'mod': lambda: push(pop() % pop()),
            '<': lambda: push(pop() < pop()),
            '>': lambda: push(pop() > pop()),
            '=': lambda: push(pop() == pop()),
            '<=': lambda: push(pop() <= pop()),
            '>=': lambda: push(pop() >= pop()),
            '<>': lambda: push(pop() != pop()),
            'not': lambda: push(not pop()),
            '&': lambda: push(pop() & pop()),
            '|': lambda: push(pop() | pop()),
            '^': lambda: push(pop() ^ pop()),
            '~': lambda: push(~pop()),
            '>R': lambda: self.rpush(pop()),
            'R>': lambda: push(self.rpop()),
            'Rdrop': lambda: self.rpop(),
            'Rdup': lambda: self.rpush(self.rstack[-1]),
            'enter': lambda: self.enter(),
            'exit': lambda: self.exit(),
            'lit': lambda: self.do_lit(),
            '[': (lambda: self.set_compiling(False), True) # immediate
            ']': lambda: self.set_compiling(True),
            ',': lambda: self.do_comma(),
            ':': lambda: self.do_colon(),
            ';': (lambda: self.do_semicolon(), True), # immediate
            'immediate': (lambda: None, True), # immediate
            'key': lambda: push(getch()),
            'emit': lambda: putch(chr(pop())),
            'branch': lambda: self.do_branch(),
            '(#)': lambda: self.do_number(),
            '#': (['(#)'], True), # immediate
        })

    def set_compiling (self, boolean):
        self.compiling = boolean

    def execute (self, word):
        code = word.function
        if callable(code):
            word.function()
        elif iterable(code):
            pass

    def start (self):
        print(' '.join(self.dictionary.keys()))

    def enter (self):
        pass

    def exit (self):
        pass

    def do_comma (self):
        pass

    def do_colon (self):
        pass

    def do_semicolon (self):
        pass

    def do_lit (self):
        pass

    def do_branch (self):
        pass

    # Convert Python values into numbers for the VM
    def convert (self, x) -> int:
        x_type = type(x)
        if x_type == int:
            return x
        elif x_type == True:
            return -1
        elif x == False:
            return 0
        elif x_type == str:
            if len(x) == 1:
                return ord(x)
        elif x_type == bytes:
            if len(x) == 1:
                return x[0]
        raise ValueError('Cannot convert type: %s' % x_type)

    # Push to the Parameter Stack
    def push (self, x):
        x = self.convert(x)
        self.stack.append(x)
        return x

    # Pop from the Parameter Stack
    def pop (self):
        if len(self.stack):
            return self.stack.pop(-1)
        else:
            raise ValueError('Parameter Stack Underflow')

    # Pop from the Return Stack
    def rpop (self):
        if len(self.rstack):
            return self.rstack.pop(-1)
        else:
            raise ValueError('Return Stack Underflow')

    # Push to the Return Stack
    def rpush (self, x):
        self.rstack.append(x)

def main ():
    vm = VM()
    vm.start()

    vm.push('>')
    vm.execute(vm.dictionary['emit'])
    vm.execute(vm.dictionary['key'])
    vm.execute(vm.dictionary['dup'])
    vm.execute(vm.dictionary['emit'])

    vm.push(1)
    vm.execute(vm.dictionary['+'])
    vm.execute(vm.dictionary['emit'])

if __name__ == "__main__":
    main()