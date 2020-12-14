/* raz.c
 * gcc -std=c99 -Wall -o raz.exe raz.c
 * (or)
 * gcc -std=c99 -Wall -o raz.exe raz.c -DDEBUG
 */

#include <stdlib.h>
#include <ctype.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "hexdump.c"

#define INITIAL_MEMORY (8 * 1024)
#define STACK_DEPTH 64

// Op-codes of the operations for the virtual machine
enum op {
	Halt, Dup, Swap, Drop,
	ToR, FromR, Add, Nand,
	Query, Dot, Skip, Exit,
	Branch, Lit, CStore, CFetch
};

// Main number/data type is the "cell"
typedef long cell;

// Main program memory pointer
char * memory_base;
char * memory;

// The Virtual Instruction Pointer
cell ** ip;

// Data/Parameter Stack Pointer
cell ** pstack_base;
cell ** pstack;

// Return Stack Pointer
cell ** rstack_base;
cell ** rstack;

// Push to the Parameter Stack
cell pop ()
{
	(*pstack)--;
	return **pstack;
}

// Pop from the Return Stack
cell rpop ()
{
	(*rstack)--;
	return **rstack;
}

// Push to the Parameter Stack
void push (cell x)
{
	**pstack = x;
	(*pstack)++;
}

// Push to the Return Stack
void rpush (cell x)
{
	**rstack = x;
	(*rstack)++;
}

// "To R" >R, pops the Parameter Stack and pushes it to the Return Stack
void tor () { rpush(pop()); }

// "R From" R>, pops the Return Stack and pushes it to the Parameter Stack
void fromr () { push(rpop()); }

// Word to swap the top two cells on the stack
void swap ()
{
	cell top = pop();
	cell next = pop();
	push(top);
	push(next);
}

// Word to duplicate/re-push the top of the stack
void dup () { push(**pstack); }

// Word to store a Cell value at an address
void cstore ()
{
	char * addr = (char *) pop();
	*addr = pop();
}

// Word to fetch a byte value at an address
void cfetch () { push(*((char *) pop())); }

// Word to perform addition
void add () { push(pop() + pop()); }

// Word to perform bitwise and
void nand () { push(!(pop() & pop())); }

// Word to branch the instruction pointer relatively based on the top of the stack
void branch () { ip += pop(); }

// Word to skip the next instruction if the top of the stack is True (1)
void skip () { if (pop()) (*ip)++; }

// Word to get a character from input
void query () { push((cell) getchar()); }

// Word to print a character
void dot () { putchar((char) pop()); }

// Word to push the next cell in the program to the stack
void lit () { push(*(*ip + 1)); (*ip)++; }

// Word to exit the direct threaded code for a word
void exit_ () { *ip = (cell *) rpop(); }

// Execute the C code identified by an operation code
void code (cell instruction)
{
	//printf("Code\n");
	switch (instruction)
	{
		case Halt: exit(0); break;
		case Dup: dup(); break;
		case Swap: swap(); break;
		case Drop: pop(); break;
		case ToR: tor(); break;
		case FromR: fromr(); break;
		case Add: add(); break;
		case Nand: nand(); break;
		case Query: query(); break;
		case Dot: dot(); break;
		case Skip: skip(); break;
		case Exit: exit_(); break;
		case Branch: branch(); break;
		case Lit: lit(); break;
		case CStore: cstore(); break;
		case CFetch: cfetch(); break;
		default: exit(-1); break;
	}
}

// Give the command-line arguments to the virtual program by pushing them onto the Parameter Stack
void pass_args (int argc, char * argv [])
{
	push((cell) argv);
	push((cell) argc);
}

void * alloc_cells (int count)
{
	void * value = memory;
	memory += count * sizeof(cell);
}

// Initialize objects in memory
void memory_init ()
{
	// Allocate all of the initial memory
	memory_base = malloc(INITIAL_MEMORY);
	memory = memory_base;

	// Allocate for the Instruction Pointer
	ip = (cell **) alloc_cells(1);

	// Allocate the Parameter Stack Pointers
	pstack_base = (cell **) alloc_cells(1);
	pstack = (cell **) alloc_cells(1);

	// Allocate the Return Stack Pointers
	rstack_base = (cell **) alloc_cells(1);
	rstack = (cell **) alloc_cells(1);

	// Allocate the Parameter Stack
	*pstack_base = (cell *) alloc_cells(STACK_DEPTH);
	*pstack = *pstack_base;

	// Allocate the Return Stack
	*rstack_base = (cell *) alloc_cells(STACK_DEPTH);
	*rstack = *rstack_base;

	// Set the Instruction Pointer to point to after the Return Stack
	*ip = (cell *) memory;
}

// Start executing the virtual code
void load_bootcode ()
{
	cell boot_code [] = {

	};
	memcpy(memory, boot_code, sizeof(boot_code));
}

int main (int argc, char * argv [])
{
	memory_init();
	pass_args(argc, argv);
	load_bootcode();
	while (1)
	{
		code(**ip);
		(*ip)++;
	}
}
