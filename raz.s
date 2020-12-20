/*
Registers
R8	H / here
R9	The top of the Parameter Stack (TOS)
R10	working register (w), contains the address of the word at the beginning of a virtual call
R11	next virtual instruction
R12	return stack pointer
R13/sp	parameter stack pointer
R14/lr	ARM link register
R15/pc	ARM program counter
*/
	.macro NEXT	// do the next virtual instruction
	ldr r10, [r11]	//	(IP) -> W	fetch memory pointed by IP into "W" register
	add r11, #4	//	IP+2 -> IP	advance IP (assuming 2-byte addresses)
	b r10		//	JP (W)		jump to the address in the W register
	.endm

	.macro R_push, reg	// Push the given register onto the Return Stack
	str \reg , [r12]
	add r12, #4
	.endm

	.macro R_pop, reg	// Pop the top of the Return Stack into the given register
	ldr \reg , [r12]
	sub r12, #4
	.endm

	.macro defword label, name, namelen, flags=0
	.section .data
	.align 2
	.global name_\label
name_\label :
	.int link
	.set link, \label _name
	.byte \flags
	.byte \namelen
	.ascii "\name"
	.section .text
	.align 2
	.global code_\label
code_\label :
	.endm

enter: // direct threaded code word interpreter
	R_push r11
	add r11, r10, #4
	NEXT

	defword exit, "exit", 4	// return from colon definition
	R_pop r11
	NEXT

	defword drop, "drop", 4	// drop/discard the TOS
	pop {r9}
	NEXT

	defword dup, "dup", 3	// duplicate the TOS
	push {r9}
	NEXT

	defword swap, "swap", 4 // swap the top two cells of the Parameter Stack
	pop {r0}
	push {r9}
	mov r9, r0
	NEXT

	defword add, "+", 1	// add the top two cells of the Parameter Stack
	pop {r0}
	add r9, r0
	NEXT

	defword plusone, "+1", 2// increment the TOS
	add r9, #1
	NEXT

	defword neg, "neg", 3	// Negate the TOS
	mov r0, 0
	sub r0, r9
	mov r9, r0
	NEXT

	defword sub, "-", 1
	pop {r0}
	sub r0, r9
	mov r9, r0
	NEXT

	defword minusone, "-1", 2// decrement the TOS
	sub r9, #1
	NEXT

	defword mul, "*", 1
	pop {r0}
	mov r1, r9
	mul r9, r0, r1
	NEXT

	defword bit_or, "|", 1	// bitwise or
	pop {r0}
	orr r9, r0
	NEXT

	defword bit_and, "&", 1	// bitwise and
	pop {r0}
	and r9, r0
	NEXT

	defword bit_xor, "x|", 2// bitwise xor
	pop {r0}
	eor r9, r0
	NEXT

	defword invert, "~", 1	// bitwise invert
	mvn r9, r9
	NEXT

	defword div, "/", 1	// Integer division
	// TODO
	NEXT

	defword mod, "mod", 3	// Integer modular math, [R0 % R9]
	pop {r0}		// Number to be divided
	mov r1, r9
	cmp r0, r1
	blt mod_end
mod_while:
	sub r0, r1
	cmp r0, r1
	bge mod_while
mod_end:
	mov r9, r0
	NEXT

	defword lit, "lit", 3	// Push the next instruction onto the stack
	push {r9}
	ldr r9, [r11]
	add r11, #4
	NEXT

	defword store, "!", 1	// store cell to memory
	pop {r0}
	str r0, [r9]
	pop {r9}
	NEXT

	defword cstore, "c!", 2	// store character/byte to memory
	pop {r0}
	str r0, [r9]
	pop {r9}
	NEXT

	defword fetch, "@", 1	// fetch cell from memory
	ldr r9, [r9]
	NEXT

	defword cfetch, "c@", 2	// fetch character/byte from memory
	ldrb r9, [r9]
	NEXT

	defword branch, "branch", 6 // get the TOS and increment the instruction pointer by it
	add r11, r9
	pop {r9}
	NEXT

	defword lshift, "<<", 2	// left shift
	pop {r0}
	lsl r0, r9
	mov r9, r0
	NEXT

	defword rshift, ">>", 2	// right shift
	pop {r0}
	lsr r0, r9
	mov r9, r0
	NEXT

	defword to_r, ">R", 2	// mov the TOS to the Return Stack
	R_push r9
	pop {r9}
	NEXT

	defword from_r, "R>", 2	// Pop the top of the Return Stack and push it to the Parameter Stack
	push {r9}
	R_pop r9
	NEXT

	defword rspfetch, "RSP@", 4	// Push the Return Stack Pointer 
	push {r9}
	mov r9, r12
	NEXT

	defword rspstore, "RSP!", 4	// Set the Return Stack Pointer to the Top Of Stack
	mov r12, r9
	pop {r9}
	NEXT

	defword pspfetch, "PSP@", 4	// Push the Parameter Stack Pointer 
	push {r9}
	mov r9, r13
	NEXT

	defword pspstore, "PSP!", 4	// Set the Parameter Stack Pointer to the Top Of Stack
	mov r13, r9
	pop {r9}
	NEXT

	defword emit, "emit", 4		// Emit a character
	mov r0, r9
	pop {r9}
	bl _emit
	NEXT
_emit:
	// TODO: print the character in R0
	bx lr

	defword key, "key", 3		// Get a character
	bl _key
	push {r9}
	mov r9, r0
	NEXT
_key:
	// TODO: get a character from input
	bx lr

	defword wait, "wait", 4		// wait a few cycles (sleep)
	// TODO
	NEXT

	defword here, "here", 4		// get the current compilation pointer
	push {r9}
	mov r9, r8
	NEXT

	defword hereat, "here@", 4	// get the value at here
	push {r9}
	ldr r9, [r8]
	NEXT

	defword hereat, "herec@", 4	// get the char value at here
	push {r9}
	ldrb r9, [r8]
	NEXT

	defword herebang, "here!", 4	// set the value at here
	str r9, [r8]
	pop {r9}
	NEXT

	defword herebang, "here!", 4	// set the value at here
	str r9, [r8]
	pop {r9}
	NEXT

	defword herebangplus, "here!+", 5	// set the value at here and increment here
	str r9, [r8]
	pop {r9}
	add r8, #4
	NEXT

	defword tick, "'", 1 // get the code address of the next word in source
	// TODO
	NEXT

	defword comma, ",", 1
	str r8, r9
	add r8, #4
	pop {r9}
	NEXT

	defword ccomma, "c,", 2
	strb r8, r9
	add r8, #1
	pop {r9}
	NEXT

	defword create, "create", 6
	NEXT

	defword colon, ":", 1
	b enter
	// TODO write the virtual code
	NEXT

	.global _start
_start:
	mov r7, 0
	swi 0

