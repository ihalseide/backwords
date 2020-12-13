.section .text
.macro NEXT // do the next instruction, which could be Forth or Assembly
	ldr r0, [r11]
	ldr r1, [r0]
	add r11, #4
	b r1
.endm
.macro DOCOL // Forth interpreter
	bl RSP_push
	add r11, r0, #4
	NEXT
.endm
.macro RSP_push // put the value of R11 onto the return stack
	str r11, [r12]
	add r12, #4
	bx lr
.endm
.macro RSP_pop // take the return stack pointer into R11
	ldr r11, [r12]
	sub r12, #4
	bx lr
.endm
exit_code: // return from subroutine
	bl RSP_pop
	NEXT
drop_code: // remove the top value on the stack
	pop {r0}
	NEXT
dup_code: // push the top value of the stack again
	pop {r0}
	push {r0, r0}
	NEXT
swap_code: // switch the top two values on the stack
	pop {r0}
	pop {r1}
	push {r0, r1}
	NEXT
over_code: // push the second value on the stack back
	pop {r0}
	pop {r1}
	push {r1, r0, r1}
	NEXT
add_code: // add the top two values on the stack
	pop {r0}
	pop {r1}
	add r0, r1
	push {r0}
	NEXT
sub_code: // subtract the second value from the first
	pop {r0}
	pop {r1}
	sub r0, r1
	push {r0}
	NEXT
mul_code: // multiply the top two values of the stack
	pop {r0}
	pop {r1}
	mul r2, r0, r1
	push {r2}
	NEXT
or_code: // bitwise or the top two values of the stack
	pop {r0}
	pop {r1}
	orr r0, r1
	push {r0}
	NEXT
and_code: // bitwise and the top two values of the stack
	pop {r0}
	pop {r1}
	and r0, r1
	push {r0}
	NEXT
xor_code: // bitwise xor the top two values of the stack
	pop {r0}
	pop {r1}
	eor r0, r1
	push {r0}
	NEXT
not_code: // bitwise invert/not the top of the stack
	pop {r0}
	mvn r0, r0
	push {r0}
	NEXT
lit_code: // push the next instruction to the stack
	ldr r0, [r11]
	add r11, #4
	push {r0}
	NEXT
store_code: // store a word to memory
	pop {r0}
	pop {r1}
	str r1, [r0]
	NEXT
storebyte_code: // store a byte of memory
	pop {r0}
	pop {r1}
	strb r1, [r0]
	NEXT
fetch_code: // fetch a word from memory
	pop {r0}
	ldr r0, [r0]
	push {r0}
	NEXT
fetchbyte_code: // fetch a byte of memory
	pop {r0}
	ldrb r0, [r0]
	push {r0}
	NEXT
branch_code: // modify next instruction pointer by adding the value of the next instruction
	ldr r0, [r11]
	add r11, r0
	NEXT
zbranch_code: // branch if top of stack is 0
	pop {r0}
	cmp r0, #0
	beq branch_code
	NEXT
lshift_code: // logical shift left (*2)
	pop {r0}
	pop {r1}
	lsl r1, r0
	push {r1}
	NEXT
rshift_code: // logical shift right (/2)
	pop {r0}
	pop {r1}
	lsr r1, r0
	push {r1}
	NEXT

.global _start
_start:
reset:
	b reset

.section .data
.set link, 0
drop:
	.int =link
	.set link, drop
	.int 4
	.ascii "drop"
	.int drop_code
dup:
	.int =link
	.set link, dup
	.int 3
	.ascii "dup"
	.int dup_code
swap:
	.int =link
	.set link, swap
	.int 4
	.ascii "swap"
	.int swap_code
over:
	.int =link
	.set link, over
	.int 4
	.ascii "over"
	.int over_code
add:
	.int =link
	.set link, add
	.int 1
	.ascii "+"
	.int add_code
sub:
	.int =link
	.set link, sub
	.int 1
	.ascii "-"
	.int sub_code
mul:
	.int =link
	.set link, mul
	.int 1
	.ascii "*"
	.int mul_code
or:
	.int =link
	.set link, or
	.int 1
	.ascii "|"
	.int or_code
and:
	.int =link
	.set link, and
	.int 1
	.ascii "&"
	.int and_code
xor:
	.int =link
	.set link, xor
	.int 1
	.ascii "^"
	.int xor_code
not:
	.int =link
	.set link, not
	.int 1
	.ascii "~"
	.int not_code
lit:
	.int =link
	.set link, lit
	.int 1
	.ascii "'"
	.int lit_code
store:
	.int =link
	.set link, store
	.int 1
	.ascii "!"
	.int store_code
storebyte:
	.int =link
	.set link, storebyte
	.int 2
	.ascii "b!"
	.int storebyte_code
fetch:
	.int =link
	.set link, fetch
	.int 1
	.ascii "@"
	.int fetch_code
fetchbyte:
	.int =link
	.set link, fetchbyte
	.int 2
	.ascii "b@"
	.int fetchbyte_code
branch:
	.int = link
	.set link, branch
	.int 6
	.ascii "branch"
	.int branch_code
zbranch:
	.int =link
	.set link, zbranch
	.int 7
	.ascii "0branch"
	.int zbranch_code
