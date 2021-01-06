from char_io import getch

# Convert Python values into numbers for the VM
def to_int (self, x) -> int:
    if type(x) == int:
        return x
    elif type(x) == str or type(x) == bytes:
        if len(x) == 1:
            return ord(str(x)[0])
    elif type(x) == bool:
        return -1 if x else 0
    raise ValueError('Cannot convert type %s to int' % type(x))

class Machine:
    '''Virtual machine'''

    def __init__ (self):
        # Parameter Stack
        self.stack = []
        # Return Stack
        self.rstack = []
        # Code / instructions
        self.instructions = []
        # Virtual Instruction Pointer / Index
        self.ip = 0
        # Memory list and memory dictionary
        self.memory = []
        self.dict_memory = {}
        # Word / Instruction dictionary
        push, pop = self.push, self.pop
        self.dictionary = {
            '*mem': self.make_mem,
            '*dict': self.make_dict,
            'halt': self.halt,
            'dup': self.dup,
            'drop': lambda: pop(),
            'swap': lambda: self.swap(),
            'topple': self.topple,
            '+': lambda: push(pop() + pop()),
            '++': lambda: push(pop() + 1),
            '-': lambda: push(pop() - pop()),
            '--': lambda: push(pop() - 1),
            '*': lambda: push(pop() * pop()),
            '**': lambda: push(pop() ** pop()),
            '/': lambda: push(pop() / pop()),
            '%': lambda: push(pop() % pop()),
            '<': lambda: push(pop() < pop()),
            '>': lambda: push(pop() > pop()),
            '=': lambda: push(pop() == pop()),
            '<=': lambda: push(pop() <= pop()),
            '>=': lambda: push(pop() >= pop()),
            '<>': lambda: push(pop() != pop()),
            'and': self.and_,
            'or': self.or_,
            'not': lambda: push(not pop()),
            '&': lambda: push(pop() & pop()),
            '|': lambda: push(pop() | pop()),
            '^': lambda: push(pop() ^ pop()),
            '~': lambda: push(~ pop()),
            '>R': lambda: self.rpush(pop()),
            'R>': lambda: push(self.rpop()),
            'Rdrop': lambda: self.rpop(),
            'Rdup': lambda: self.rpush(self.rstack[-1]),
            'key': lambda: push(getch()),
            'utf8': lambda: push(pop().decode("utf-8")),
            'input': lambda: push(input()),
            'print': lambda: print(end=pop()),
            'branch': self.branch,
            '#': self.literal,
            '!': self.store,
            ':!': self.dict_store,
            '@': self.fetch,
            ':@': self.dict_fetch,
            'str': push(str(pop())),
            'int': push(int(pop())),
        }

    def make_mem (self):
        self.memory = [None for _ in range(self.pop())]

    def make_dict (self):
        self.dict_memory = {}

    def store (self):
        x, y = self.pop(), self.pop()
        self.memory[y] = x

    def fetch (self):
        self.push(self.memory[self.pop()])

    def dict_store (self):
        x, y = self.pop(), self.pop()
        self.dict_memory[y] = x

    def dict_fetch (self):
        self.push(self.dict_memory[self.pop()])

    def or_ (self):
        a, b = self.pop(), self.pop()
        self.push(a or b)

    def and_ (self):
        a, b = self.pop(), self.pop()
        self.push(a and b)

    def topple (self):
        # Topple / clear the stack
        self.stack = []

    def halt (self):
        self.ip = None

    def dup (self):
        push(self.stack[-1])

    def branch (self):
        self.ip += self.pop()

    def literal (self):
        self.push(self.ip + 1)
        self.ip += 1

    def compile_instruction (self, name):
        self.append_instruction(self.dictionary[name])

    def append_instruction (self, i):
        self.instructions.append(i)

    def add_word (self, name, function):
        self.dictionary[name] = function

    def step (self):
        word = self.instructions[self.ip]
        word()
        self.ip += 1

    def run (self):
        while self.halt != self.instructions[self.ip]:
            self.step()

    # Push to the Parameter Stack
    def push (self, x):
        self.stack.append(x)
        return x

    # Pop from the Parameter Stack
    def pop (self):
        if len(self.stack):
            return self.stack.pop(-1)
        else:
            raise ValueError('Parameter Stack Underflow')

    # Push to the Return Stack
    def rpush (self, x):
        self.rstack.append(x)

    # Pop from the Return Stack
    def rpop (self):
        if len(self.rstack):
            return self.rstack.pop(-1)
        else:
            raise ValueError('Return Stack Underflow')


