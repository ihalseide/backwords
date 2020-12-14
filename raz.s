	.macro NEXT // do the next instruction
	ldr r0, [r11]
	ldr r1, [r0]
	add r11, #4
	b r1
	.endm

	.macro DOCOL // direct threaded code word interpreter
	bl RSP_push
	add r11, r0, #4
	NEXT
	.endm

	.macro RSP_push // put the value of R11 onto the return stack
	str r11, [r12]
	add r12, #4
	.endm

	.macro RSP_pop // take the return stack pointer into R11
	ldr r11, [r12]
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

	defword exit, "exit", 4
	RSP_pop
	NEXT

	defword drop, "drop", 4
	pop {r0}
	NEXT

	defword dup, "dup", 3
	pop {r0}
	push {r0, r0}
	NEXT

	defword swap, "swap", 4
	pop {r0}
	pop {r1}
	push {r0, r1}
	NEXT

	defword add, "+", 1
	pop {r0}
	pop {r1}
	add r0, r1
	push {r0}
	NEXT

	defword sub, "-", 1
	pop {r0}
	pop {r1}
	sub r0, r1
	push {r0}
	NEXT

	defword mul, "*", 1
	pop {r0}
	pop {r1}
	mul r2, r0, r1
	push {r2}
	NEXT

	defword bit_or, "|", 1
	pop {r0}
	pop {r1}
	orr r0, r1
	push {r0}
	NEXT

	defword bit_and, "&", 1
	pop {r0}
	pop {r1}
	and r0, r1
	push {r0}
	NEXT

	defword bit_xor, "x|", 2
	pop {r0}
	pop {r1}
	eor r0, r1
	push {r0}
	NEXT

	defword invert, "~", 1
	pop {r0}
	mvn r0, r0
	push {r0}
	NEXT

	defword lit, "lit", 3
	ldr r0, [r11]
	add r11, #4
	push {r0}
	NEXT

	defword store, "!", 1
	pop {r0}
	pop {r1}
	str r1, [r0]
	NEXT

	defword cstore, "c!", 2
	pop {r0}
	pop {r1}
	strb r1, [r0]
	NEXT

	defword fetch, "@", 1
	pop {r0}
	ldr r0, [r0]
	push {r0}
	NEXT

	defword cfetch, "c@", 2
	pop {r0}
	ldrb r0, [r0]
	push {r0}
	NEXT

	defword branch, "branch", 6 // get the top of the stack and increment the instruction pointer by it
	pop {r0}
	add r11, r0
	NEXT

	defword skip, "skip", 4 // skip the next instruction if the top of the stack is true
	pop {r0}
	mov r1, -1
	cmp r0, r1
	addeq r11, #4
	NEXT

	defword lshift, "<<", 2
	pop {r0}
	pop {r1}
	lsl r1, r0
	push {r1}
	NEXT

	defword rshift, ">>", 2
	pop {r0}
	pop {r1}
	lsr r1, r0
	push {r1}
	NEXT

	.global _start
_start:
	mov r7, 0
	swi 0

