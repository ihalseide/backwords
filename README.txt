= The Backwords Programming Language =

Backwords is a low level esoteric programming language. There is a data stack,
a memory tape, and a program counter. All values are bytes in the range 0 to
255, and the values wrap around. The program runs in an implicit infinite loop.
Numbers are in base 16 for compactness (the biggest number is #FF).

Creating a program in this language is pretty much like writing machine code
by hand, but with ASCII.

[https://github.com/ihalseide/backwords]

== Backwords Language Python Implementation ==

The interpreter program, written in Python, runs program files.  Example
programs are text files and start with "ex_".

== Commands ==

By default, if there are not enough numbers on the stack for the command to
execute, the program will exit. The only way that the program can exit if there
is a runtime error or if the semicolon ';' command is executed (either directly
or indirectly via the '.' command).

:	duplicates the top of the stack unless the stack is empty

0-F	multiply the top of the stack by 16 and then add either 0, 1, 2, ... or
	15

+	adds the top two numbers on the stack

-	subtracts the top two numbers on the stack

*	multiplies the top two numbers on the stack

/	divides the top two numbers on the stack

%	does modular arithmetic with the top two numbers

`	does a bitwise NOT to the top of the stack

&	does a bitwise AND to the top two values of the stack

|	does a bitwise OR to the top two values of the stack

,	emits the top of the stack as a character (97='a' etc.)

?	gets a character from input and pushes it onto the stack

;	halts the program

\	explicitly loops the program counter back to the beginning of the
	program

_	drops the top of the stack

#	pushes 0 to the stack, and is used to start a number

'	push the next character in the program to the stack

=	pushes a 255 if the top two numbers in the stack are equal, otherwise
	push a 0 (pops both numbers off of the stack)

>	is like "=" but for if the top of the stack is less than the second

<	is like "=" but for if the top of the stack is greater than the second

.	evaluates the top of the stack as a command

^	adds the top of the stack to the program counter, branch forwards

v	subtracts the top of the stack from the program counter, branch
	backwards

n	does the next command only if the top of the stack is [n]ot zero

z	does the next command only if the top of the stack is [z]ero

u	clears the stack

s	swaps the top two numbers

{	move to the previous memory section on the tape

}	move to the next memory section on the tape

@	fetches a value from the memory tape at the address given

!	get an address, then a value, and finally store the value at the
	given address in the current memory page

i	gets the instruction [top of stack] characters before the current ip

I	gets the instruction [top of stack] characters after the current ip

$	pushes the stack size (before the operation). Caution: The stack can
	hold more than 255 values, but the maximum value $ can return is 255

g	prints out the stack, for debugging

k	acts as a debug "breakpoint"

"	pushes the contents of a string up to the next double quote, in reverse
	order. This is useful for pushing a bunch of values onto the stack

All other characters are ignored. "I" and "i" allow the program to read its own
source code as data. For the "{" and "}" commands, a memory tape section is 256
bytes

@COPYRIGHT ALL WRONGS RESERVED
