/* raz.c
 * gcc -std=c99 -Wall -o raz raz.c
 */

#include <stdlib.h>
#include <ctype.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "hexdump.c"

#define INITIAL_MEMORY (8 * 1024)
#define PSTACK_DEPTH 64
#define RSTACK_DEPTH 64

// Op-codes and names of thos operations for the virtual machine
// These lists should be the same size
enum op {
	Halt, Mzero, Dup, Swap, Drop, Over, Szero, Dspbang, Dspat,
	Tor, Rfrom, Rspbang, Rspat, Rzero, Add, Mul, Div_, Sub, Or,
	And, Xor, Invert, Eq, Not, True, False, Query, Dot, Branch,
	Skip, Lit, Bang, Cbang, At, Cat, Exit_, Getcell, Quit
};
// Names kept for testing
char * op_names [] = {
	"Halt", "Mzero", "Dup", "Swap", "Drop", "Over", "Szero", "Dspbang", "Dspat",
	"Tor", "Rfrom", "Rspbang", "Rspat", "Rzero", "Add", "Mul", "Div_", "Sub", "Or",
	"And", "Xor", "Invert", "Eq", "Not", "True", "False", "Query", "Dot", "Branch",
	"Skip", "Lit", "Bang", "Cbang", "At", "Cat", "Exit_", "Getcell", "Quit"
};

// Main number/data type is the "cell"
typedef long cell;

// Main program memory pointer
char * memory_base;
char * memory;

// The Virtual Instruction Pointer
cell * ip;

// Data/Parameter Stack Pointer
cell * pstack_base;
cell * pstack;

// Return Stack Pointer
cell * rstack_base;
cell * rstack;

#if DEBUG
void print_stack ()
{
	printf("<Stack:");
	cell * p = pstack_base;
	while (p < pstack)
	{
		printf(" %ld", *p);
		p++;
	}
	printf(">");
}
#endif

// Push to the Parameter Stack
void push (cell x)
{
	*pstack = x;
	pstack++;
	assert((pstack - pstack_base) < PSTACK_DEPTH);
}

// Push to the Parameter Stack
cell pop ()
{
	pstack--;
	assert(pstack >= pstack_base);
	return *pstack;
}

// Push to the Return Stack
void rpush (cell x)
{
	*rstack = x;
	rstack++;
	assert((rstack - rstack_base) < RSTACK_DEPTH);
}

// Pop from the Return Stack
cell rpop ()
{
	rstack--;
	assert(pstack >= pstack_base);
	return *rstack;
}

// Word to store a Cell value at an address
void bang ()
{
	cell * addr = (cell *) pop();
	cell val = pop();
	*addr = val;
}

// Word to store a byte value at an address
void cbang ()
{
	char * addr = (char *) pop();
	char val = (char) pop();
	*addr = val;
}

// Word to fetch a cell value at an address
void at ()
{
	push(*((cell *) pop()));
}

// Word to fetch a byte value at an address
void cat ()
{
	push(*((char *) pop()));
}

// Word for equality comparison of the top 2 cells
void eq ()
{
	push(pop() == pop());
}

// Word to push the value of true to the Parameter Stack
// True is 1, as per the standard for C
void true ()
{
	push(1);
}

// Word to push the value of false to the Parameter Stack
// False is 0, as per the standard for C
void false ()
{
	push(0);
}

// Word for converting between True or False, which are 1 or 0 respectively
void not ()
{
	push(!pop());
}

// Word to swap the top two cells on the stack
void swap ()
{
	int top = pop();
	int next = pop();
	push(top);
	push(next);
}

// Word to duplicate/re-push the top of the stack
void dup ()
{
	push(*(pstack - 1));
}

// Word to discard the top of the stack
void drop ()
{
	pop();
}

// Word to duplicate the second-from-the-top cell in the stack
void over ()
{
	push(*(pstack - 2));
}

// Word to perform addition
void add ()
{
	push(pop() + pop());
}

// Word to perform subtraction
void sub ()
{
	push(pop() - pop());
}

// Word to perform multiplication
void mul ()
{
	push(pop() * pop());
}

// Word to perform division
void div_ ()
{
	push(pop() / pop());
}

// Word to perform bitwise and
void and ()
{
	push(pop() & pop());
}

// Word to perform bitwise or
void or ()
{
	push(pop() | pop());
}

// Word to perform bitwise xor
void xor ()
{
	push(pop() ^ pop());
}

// Word to perform bitwise not
void invert ()
{
	push(~pop());
}

// Word to shift the value of a cell left
void lshift ()
{
	push(pop() << pop());
}

// Word to shift the value of a cell right
void rshift ()
{
	push(pop() >> pop());
}

// Word to branch the instruction pointer relatively based on the top of the stack
void branch ()
{
	ip += pop();
}

// Word to skip the next instruction if the top of the stack is True (1)
void skip ()
{
	if (pop())
	{
		ip++;
	}
}

// Word to get a character from input
void query ()
{
	push((cell) getchar());
}

// Word to print a character
void dot ()
{
	putchar((char) pop());
}

// Word to push the next cell in the program to the stack
void lit ()
{
	push(*ip);
	ip++;
}

// Word to exit the direct threaded code for a word
void exit_ ()
{
	ip = (cell *) rpop();
}

// "To R" >R, pops the Parameter Stack and pushes it to the Return Stack
void tor ()
{
	rpush(pop());
}

// "R From" R>, pops the Return Stack and pushes it to the Parameter Stack
void rfrom ()
{
	push(rpop());
}

// Word to get the address of the bottom of the Parameter Stack
void szero ()
{
	push((cell) pstack_base);
}

// Word to get the address of the bottom of the Return Stack
void rzero ()
{
	push((cell) rstack_base);
}

// Word to get the address of the bottom of Memory
void mzero ()
{
	push((cell) memory_base);
}

// Word to set the Data Stack Pointer, a.k.a the Parameter Stack Pointer to a value
void dspbang ()
{
	pstack = (cell *) pop();
}

// Word to fetch the Data Stack Pointer, a.k.a the Parameter Stack Pointer
void dspat ()
{
	push((cell) pstack);
}

// Word to set the Return Stack Pointer to a value
void rspbang ()
{
	pstack = (cell *) pop();
}

// Word to fetch the Return Stack Pointer
void rspat ()
{
	push((cell) rstack);
}

void code (cell);

void interpret ()
{
	cell w = *ip;
	ip++;
	code(w);
}

// Start the virtual program by invoking the inner Interpreter
void quit ()
{
	// Reset the Return Stack
	rstack = rstack_base;
	// Infinitely execute the virtual program
	while (1)
	{
		interpret();
	}
}

void halt ()
{
#if DEBUG
	printf("\nreceived code 0x00 (halt)\n");
	printf("Print memory dump? (y/n) > ");
	char c = getchar();
	if (c == 'y' || c == 'Y')
	{
		hex_dump(memory_base, 2 * 1024);
	}
#endif
	putchar('\n');
	exit(-1);
}

void getcell ()
{
	push(sizeof(cell));
}

// Used in the `code' function if an invalid code is reached
void bad_code (cell instruction)
{
	fprintf(stderr, "bad code: %ld at address: %p\n", instruction, ip);
	exit(-1);
}

// Execute the C code identified by an operation code
void code (cell instruction)
{
#if DEBUG
	print_stack();
	// Note: this is a range check with the first and the last op-code
	if (Halt < instruction && instruction <= Quit)
	{
		if (instruction == Lit)
		{
			cell literal = *ip;
			if (isprint((char) literal))
			{
				printf("<Lit %ld = '%c'>\n", literal, (char) literal);
			}
			else
			{
				printf("<Lit %ld>\n", literal);
			}
		}
		else
		{
			printf("<%s>\n", op_names[instruction]);
		}
	}
#endif
	switch (instruction)
	{
		case Halt:    halt();    break;
		case Mzero:   mzero();   break;
		case Dup:     dup();     break;
		case Swap:    swap();    break;
		case Drop:    drop();    break;
		case Over:    over();    break;
		case Szero:   szero();   break;
		case Dspbang: dspbang(); break;
		case Dspat:   dspat();   break;
		case Tor:     tor();     break;
		case Rfrom:   rfrom();   break;
		case Rspbang: rspbang(); break;
		case Rspat:   rspat();   break;
		case Rzero:   rzero();   break;
		case Add:     add();     break;
		case Mul:     mul();     break;
		case Div_:    div_();    break;
		case Sub:     sub();     break;
		case Or:      or();      break;
		case And:     and();     break;
		case Xor:     xor();     break;
		case Invert:  invert();  break;
		case Eq:      eq();      break;
		case Not:     not();     break;
		case True:    true();    break;
		case False:   false();   break;
		case Query:   query();   break;
		case Dot:     dot();     break;
		case Branch:  branch();  break;
		case Skip:    skip();    break;
		case Lit:     lit();     break;
		case Bang:    bang();    break;
		case Cbang:   cbang();   break;
		case At:      at();      break;
		case Cat:     cat();     break;
		case Exit_:   exit_();   break;
		case Getcell: getcell(); break;
		case Quit:    quit();    break;
		default: bad_code(instruction);
	}
}

// Give the command-line arguments to the virtual program by pushing them onto the Parameter Stack
void pass_args (int argc, char * argv [])
{
	push(argc);
	push((cell) argv);
	assert(*(pstack - 1) == ((cell) argv));
	assert(*(pstack - 2) == argc);
#if DEBUG
	printf("Argument count: %d\n", argc);
	printf("Address of argument values: %p\n", argv);
#endif
}

// Initialize memory with a call to MALLOC
// Note: the memory_base pointer should not change
// Note: the memory pointer should change as things allocate from it
void memory_init ()
{
	memory_base = malloc(INITIAL_MEMORY);
	memory = memory_base;
#if DEBUG
	printf("Memory begins at %p\n", memory_base);
#endif
}

// Initialize the Parameter Stack by taking from memory from the memory pointer
void pstack_init ()
{
	pstack_base = (cell *) memory;
	pstack = pstack_base;
	memory += PSTACK_DEPTH * sizeof(cell);
#if DEBUG
	printf("Parameter/Data Stack starts at %p\n", pstack_base);
#endif
}

// Initialize the Return Stack by taking from memory from the memory pointer
void rstack_init ()
{
	rstack_base = (cell *) memory;
	rstack = rstack_base;
	memory += RSTACK_DEPTH * sizeof(cell);
#if DEBUG
	printf("Return Stack starts at %p\n", rstack_base);
#endif
}

// Start executing the virtual code
void load_bootcode ()
{
	cell boot_code [] = {
		Drop, Drop,
		Lit, '?',
		Lit, '?',
		Lit, 1,
		Add,
		Dup, Dot,
		Tor,
		Dot,
		Halt
	};
	memcpy(memory, boot_code, sizeof(boot_code));
#if DEBUG
	printf("bootcode is %ld chars or %ld cells long\n", sizeof(boot_code), sizeof(boot_code)/sizeof(boot_code[0]));
#endif
}

// Initialize the Instruction Pointer
void ip_init ()
{
	ip = (cell *) memory;
}

int main (int argc, char * argv [])
{
#if DEBUG
	printf("Note: this Raz is compiled in debug mode\n");
	printf("Press ENTER to continue...");
	getchar();
#endif
	memory_init();
	pstack_init();
	rstack_init();
	pass_args(argc, argv);
	load_bootcode();
	ip_init();
	quit();
}
