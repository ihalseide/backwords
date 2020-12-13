/* raz.c
 */

#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "hexdump.c"

#define INITIAL_MEMORY 8 * 1024
#define PSTACK_DEPTH 64
#define RSTACK_DEPTH 64

// Main number/data type is the "cell"
typedef long int cell;

// (Virtual) Instruction Pointer
cell * ip;

// Main program memory pointer
char * memory;
char * memory_base;

// Compilation pointer
char * phere;

// Data Stack Pointer / Parameter Stack Pointer
cell * pstack;

// Return Stack Pointer
cell * rstack;

void next ()
{

}

// Push to the parameter stack
void push (cell x)
{
	*pstack = x;
	pstack++;
}

// Push to the parameter stack
cell pop ()
{
	pstack--;
	return *pstack;
}

// Push to the return stack
void rpush (cell x)
{
	*rstack = x;
	rstack++;
}

// Pop from the return stack
cell rpop ()
{
	rstack--;
	return *rstack;
}
// Word to store a cell value at an address
void bang ()
{
	cell * addr = (cell *) pop();
	cell val = pop();
	*addr = val;
}

// Word to set a byte at an address
void cbang ()
{
	char * addr = (char *) pop();
	char val = (char) pop();
	*addr = val;
}

// Word to fetch a value at an address
void at ()
{
	push(*((cell *) pop()));
}

// Word to fetch a byte at an address
void cat ()
{
	push(*((char *) pop()));
}

// Word to compile a cell at Here
void comma ()
{

}

// Word to compile a byte at Here
void ccomma ()
{

}

// Word for equality comparison of the top 2 cells
void eq ()
{
	push(pop() == pop());
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
	next();
}

void memory_init ()
{
	memory_base = malloc(INITIAL_MEMORY);
	memory = memory_base;

	phere = memory;
	memory++;
}

void pstack_init ()
{
	pstack = memory;
	memory += PSTACK_DEPTH;
}

void rstack_init ()
{
	rstack = memory;
	memory += RSTACK_DEPTH;
}

// Add the definition for a word defined in this C program
void add_cword (const char * word, void (* func) (void))
{
	struct word * new = (struct word *) phere;
	new->link = (struct word *) link;
	link = (struct word *) phere;
	phere += sizeof(struct word);
	int len = strlen(word);
	new->length = len;
	for (int i = 0; i < 27; i++)
	{
		char c;
		if (i < len)
		{
			c = word[i];
		}
		else
		{
			c = ' ';
		}
		new->name[i] = c;
	}
	new->code = func;
}

// Check if two length-encoded strings are equal
int str_eq_ (const char * str1, int len1, const char * str2, int len2)
{
	if (len1 == len2)
	{
		for (int i = 0; i < len1; i++)
		{
			if (str1[i] != str2[i])
			{
				return 0;
			}
		}
		return 1;
	}
	else
	{
		return 0;
	}
}

// Word to compare two length-encoded strings being equal
void dollareq ()
{
	int len1 = (int) pop();
	char * str1 = (char *) pop();
	int len2 = (int) pop();
	char * str2 = (char *) pop();
	push((cell) str_eq_(str1, len1, str2, len2));
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

// Code to find a word definition with a given name
struct word * find_ (char * want_str, int want_len)
{
	struct word * follow_link = (struct word *) link;
	assert(follow_link != NULL);
	assert(strlen(want_str) == want_len);
	while (follow_link)
	{
		int len = follow_link->length;
		char * str = follow_link->name;
		if (str_eq_(want_str, want_len, str, len))
		{
			return follow_link;
		}
		else
		{
			follow_link = follow_link->link;
		}
	}
	return NULL;
}

// Word for finding a word `find_'
void find ()
{
	char * str = (char *) pop();
	int length = (int) pop();
	push((cell) find_(str, length));
}

// Word to get the address of here
void here ()
{
	push((cell) phere);
}

// Word to get the address of the bottom of the Parameter Stack
void szero ()
{
	push((cell) pstack);
}

// Word to get the address of the bottom of the Return Stack
void rzero ()
{
	push((cell) rstack);
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

void find_cword ()
{

}

void code ()
{
	cell instruction = pop();
	switch (instruction)
	{
		case 0:
			// "M0" :: mzero
			mzero();
			break;
		case 1:
			// "here" :: here
			here();
			break;
		case 2:
			// "dup" :: dup
			dup();
			break;
		case 3:
			// "swap" :: swap
			swap();
			break;
		case 4:
			// "drop" :: drop
			drop();
			break;
		case 5:
			// "over" :: over
			over();
			break;
		case 6:
			// "S0" :: szero
			szero();
			break;
		case 7:
			// "DSP!" :: dspbang
			dspbang();
			break;
		case 8:
			// "DSP@" :: dspat
			dspat();
			break;
		case 9:
			// ">R" :: tor
			tor();
			break;
		case 10:
			// "R>" :: rfrom
			rfrom();
			break;
		case 11:
			// "RSP!" :: rspbang
			rspbang();
			break;
		case 12:
			// "RSP@" :: rspat
			rspat();
			break;
		case 13:
			// "R0" :: rzero
			rzero();
			break;
		case 14:
			// "+" :: add
			add();
			break;
		case 15:
			// "*" :: mul
			mul();
			break;
		case 16:
			// "/" :: div_
			div_();
			break;
		case 17:
			// "-" :: sub
			sub();
			break;
		case 18:
			// "|" :: or
			or();
			break;
		case 19:
			// "&" :: and
			and();
			break;
		case 20:
			// "^" :: xor
			xor();
			break;
		case 21:
			// "~" :: invert
			invert();
			break;
		case 22:
			// "=" :: eq
			eq();
			break;
		case 23:
			// "not" :: not
			not();
			break;
		case 24:
			// "true" :: true
			true();
			break;
		case 25:
			// "false" :: false
			false();
			break;
		case 26:
			// "?" :: query
			query();
			break;
		case 27:
			// "." :: dot
			dot();
			break;
		case 28:
			// "branch" :: branch
			branch();
			break;
		case 29:
			// "skip" :: skip
			skip();
			break;
		case 30:
			// "lit" :: lit
			lit();
			break;
		case 31:
			// "find" :: find
			find();
			break;
		case 32:
			// "!" :: bang
			bang();
			break;
		case 33:
			// "c!" :: cbang
			cbang();
			break;
		case 34:
			// "@" :: at
			at();
			break;
		case 35:
			// "c@" :: cat
			cat();
			break;
		case 36:
			// "," :: comma
			comma();
			break;
		case 37:
			// "c," :: ccomma
			ccomma();
			break;
		case 38:
			// "$= :: dollareq
			dollareq();
			break;
		case 39:
			// "exit" :: exit_
			exit_();
			break;
		default:
			fprintf(stderr, "unknown instruction: #%d", instruction);
			break;
	}
}

// Give the command-line arguments to the virtual program by pushing them onto the Parameter Stack
void pass_args (int argc, char * argv [])
{
	push(argc);
	push((cell) argv);
	assert(*(pstack - 1) == ((cell) argv));
	assert(*(pstack - 2) == argc);
}

int main (int argc, char * argv [])
{
	memory_init();
	pstack_init();
	rstack_init();

	pass_args(argc, argv);
}
