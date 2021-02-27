= The Backwords Programming Language =

Backwords [https://github.com/ihalseide/backwords] is a character-based low
level esoteric programming language of my own invention. There is a data stack,
a memory tape, and a program counter. All values are bytes in the range 0 to
255, and the values wrap around. The program runs in an implicit infinite loop.
Numbers are in base 16 for compactness (the biggest number is #FF). Also, you
can write comments in the file anywhere that the comment won't affect the state
of the program either because the comment has no command characters, or the
program jumps over the comment with '^' or 'v', or the program never reaches
the comment because the program halts (usually because of ';') before it reads
the comment.

WARNING: Creating a program in this language is pretty much like writing
machine code by hand, but with ASCII. Program at the risk of your own
sanity!

And, of course, every command has a SUPER USEFUL M[N]EMONIC just like assembly!
/s ;-)

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

/	performs floor division on the top two numbers on the stack

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

=	push 255 if the top two numbers in the stack are equal, otherwise
	push a 0 (pops both numbers off of the stack)

>	push 255 if the top of the stack is less than the second, otherwise
	push 0 (pops both numbers off of the stack)

<	push 255 if the top of the stack is greater than the second, otherwise
	push 0 (pops both numbers off of the stack)

.	evaluates the top of the stack as a command

^	adds the top of the stack to the program counter, branch forwards
	(obviously can't branch forwards more than 256 characters)

v	subtracts the top of the stack from the program counter, branch
	backwards (obviously can't branch backwards more than 256 characters)

n	does the next command only if the top of the stack is [n]ot zero

z	does the next command only if the top of the stack is [z]ero

u	clears the stack, but I like to call it "[u]nstacking"

s	[s]waps the top two numbers

{	move to the previous memory section on the tape

}	move to the next memory section on the tape

@	fetches a value from the memory tape at the address given, called "at"

!	get an address, then a value, and finally store the value at the
	given address in the current memory page

i	gets the instruction [top of stack] characters before the current ip

I	gets the instruction [top of stack] characters after the current ip

$	pushes the stack size (before the operation). Caution: The stack can
	hold more than 255 values, but the maximum value $ can return is 255

g	prints out the stack, for debu[g]ging

k	acts as a debug brea[k]point

"	pushes the contents of a string up to the next double quote, but
	backwards. This is useful for pushing a bunch of values onto the stack
	at once

All other characters are ignored. "I" and "i" allow the program to read its own
source code as data. For the two { } commands, a memory tape section is 256
bytes. Also note that ' " ? # $ are the only five commands that grow the stack,
and that every other command either keeps the stack the same size or shrinks
the stack.

@COPYRIGHT ALL WRONGS RESERVED
