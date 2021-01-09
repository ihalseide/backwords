# virtual machine code

class Machine:
    '''Virtual machine'''
    def __init__ (self, memory_len, cell_size):
        self.is_started = False
        self.cell_size = cell_size # bits
        self._init_parameter_stack()
        self._init_instructions()
        self._init_memory(memory_len)
        self._init_word_dictionary()

    def _init_memory (self, length):
        self.memory = [0 for _ in range(length)]

    def _init_instructions (self):
        self.instructions = []
        # Virtual Instruction Pointer / Index
        self.ip = 0

    def _init_parameter_stack (self):
        self.stack = []

    def _init_word_dictionary (self):
        self.token_id = 0
        self.comp_dictionary = {}
        self.code_dictionary = {}
        self._add_the_words()

    def _add_the_words (self):
        # Aliases
        push, pop = self.push, self.pop
        
        self.add_word('halt', self.halt)
        self.add_word('dup', self.dup)
        self.add_word('drop', self.pop)
        self.add_word('swap', self.swap)
        self.add_word('topple', self.topple)
        self.add_word('+', lambda: push(pop() + pop()))
        self.add_word('+=1', lambda: push(pop() + 1))
        self.add_word('-', lambda: push(pop() - pop()))
        self.add_word('-=1', lambda: push(pop() - 1))
        self.add_word('*', lambda: push(pop() * pop()))
        self.add_word('**', lambda: push(pop() ** pop()))
        self.add_word('/', lambda: push(pop() / pop()))
        self.add_word('%', lambda: push(pop() % pop()))
        self.add_word('<', lambda: push(pop() < pop()))
        self.add_word('>', lambda: push(pop() > pop()))
        self.add_word('=', lambda: push(pop() == pop()))
        self.add_word('<=', lambda: push(pop() <= pop()))
        self.add_word('>=', lambda: push(pop() >= pop()))
        self.add_word('<>', lambda: push(pop() != pop()))
        self.add_word('and', self.and_)
        self.add_word('or', self.or_)
        self.add_word('not', lambda: push(not pop()))
        self.add_word('&', lambda: push(pop() & pop()))
        self.add_word('|', lambda: push(pop() | pop()))
        self.add_word('^', lambda: push(pop() ^ pop()))
        self.add_word('~', lambda: push(~ pop()))
        self.add_word('branch', self.branch)
        self.add_word('skip', self.skip)
        self.add_word('#', self.literal)
        self.add_word('!', self.store)
        self.add_word('@', self.fetch)

    def swap (self):
        t, b = self.pop(), self.pop()
        self.push(t)
        self.push(b)
        
    def top (self):
        return self.stack[-1]

    def skip (self):
        if self.pop():
            self.ip += 1

    def store (self):
        x, y = self.pop(), self.pop()
        self.memory[y] = x

    def fetch (self):
        self.push(self.memory[self.pop()])

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
        self.is_started = False

    def dup (self):
        self.push(self.top())

    def branch (self):
        self.ip += self.pop()

    def literal (self):
        self.push(self.instructions[self.ip + 1])
        self.ip += 1

    def find (self, name):
        return self.comp_dictionary.get(name)

    def compile_instruction (self, name):
        code = self.find(name)
        self.append_instruction(code)

    def append_instruction (self, i):
        if self.is_started:
            raise NotImplemented()
        else:
            self.instructions.append(i)

    def next_token (self):
        r = self.token_id
        if self.token_id > ((2 ** self.cell_size) - 1):
            raise ValueError('Token number exceeds cell max size')
        self.token_id += 1
        return r
    
    def add_word (self, name, function):
        id_ = self.next_token()
        self.comp_dictionary[name] = id_
        self.code_dictionary[id_] = function

    def start (self):
        self.is_started = True
        self.ip = 0

    def execute (self, token):
        code = self.code_dictionary[token]
        code()
        
    def step (self):
        token = self.instructions[self.ip]
        self.execute(token)
        if self.ip is not None:
            self.ip += 1

    def run (self):
        while self.is_started:
            self.step()

    def push (self, x):
        # Push to the Parameter Stack
        maxbit = (2 ** self.cell_size) - 1
        self.stack.append(min(x, maxbit))

    def pop (self):
        # Pop from the Parameter Stack
        return self.stack.pop(-1)

