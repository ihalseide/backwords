# Postfix Language `Backwords"

This is a stack-based programming language. Programs consist of a string of words.

## Words

The following is a list of words in the language, and the type of operation is sometimes written.
Nilary: takes 0 arguments from the stack
Unary: takes 1 argument from the stack
Dyadic: takes 2 arguments from the stack

Any string of digits: push the integer to the stack

'+' Dyadic addition

'-' Dyadic subtraction

'*' Dyadic multiplication

'/' Dyadic division

'~' Negation, unary

'"' Pop and discard the top of the stack, nilary

'!' Get the top of the stack and pop the stack that many times (not including the first pop), unary

'p' Unary print the top of the stack as a number

'P' Unary print the top of the stack as a character

'^' Push a character from stdin onto the stack

'#' Nilary read a decimal number from stdin

'?' Only perform the next word if the top of the stack is true

'=' Dyadic compare for equality, preserving operands

'`' Unary logical not, N -> 0, 0 -> 1

 '  Nilary push a string to the stack, delimited by 'single quotes'

'S'  Nilary print, by popping the stack until a 0 is reached
            
'\' Push the value of the next character in the program onto the stack (so `\~' will push 126 onto the stack)

';' Loop back to beginning, nilary

'$' Preserve the operands for the next operation, nilary

'x' Square the top of the stack, unary

'.' Duplicate the top of the stack, nilary

'&' Evaluate the top of the stack as a word, unary

'V': Peek at the Nth entry from the top of the stack, unary

'N' Peek at the (top)th entry in the stack, unary

' ' Spaces are ignored

'd' Decrement the top of the stack, unary

'i' Increment the top of the stack, unary

'l' Emit a newline character, nilary

't' Emit a tab character, nilary

'H' Halve the top of the stack, unary

'D' Double the top of the stack, unary

'q' Take the square root of the top of the stack, unary

## Programs to Try in 'Postfix'

Hello world
    '!dlroW ,olleH'S

Square a number with a prompt
    ':#'S#xp

Square a number without a prompt
    #xp

Add 2 given numbers
    ##+p

Double a given number
    #.+p
    #2*p

Quadratic formula
    ###.....

A Forth-like language

- Idea: implement an accessible "features" list like in LISP implementations

@COPYRIGHT ALL WRONGS RESERVED