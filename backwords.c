/* License information for this program is located at the bottom of this file */

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

#define STACK_SIZE 1024
#define INPUT_SIZE 256

/* Program input buffer */
static char input_buffer[INPUT_SIZE];
static char* stream;

/* Program's memory stack */
static long stack_values[STACK_SIZE];
static int stack_index = -1;

/*
Flag to indicate that numbers popped back from the stack should be put back
on after an operation is performed.
*/
static char preserve;

/* Convert a digit character into it's value */
char decimal_value  
(char c)
{
    return c - '0';
}

/* Increment the stack index by n, for preserving popped stack values */
void stack_unpop
(int n)
{
    stack_index += n;
}

/* Peek at the nth index from the top */
long stack_peek
(int index)
{
    return stack_values[stack_index - index];
}

/* Get the the value at the top of the stack */
long stack_top
()
{  
    return stack_values[stack_index];
}

/*
Pop the stack by moving the stack index value
(values are not actually removed, for stack preservation)
*/
long stack_pop
()
{
    if (stack_index < 0)
    {
        /* This could technically be an error, but let's just return 0 */
        return 0;
    }
    long value = stack_values[stack_index];
    stack_index--;
    return value;
}

/* Push a number to the stack */
void stack_push
(long n)
{
    stack_index++;
    stack_values[stack_index] = n;
}

/* Print the stack contents */
void stack_print
()
{
    printf("\nStack:\n");
    int i;
    if (stack_index >= 0) 
    {
        for (i = 0; i < stack_index + 1; i++)
        {
            printf("[%3d] : %ld\n", i, stack_values[i]);
        }
    }
    else
    {
        printf("Empty\n");
    }
}

void input_next
()
{
    stream++;
}

char input_char
()
{
    return *stream;
}

void input_skip_space
()
{
    while (isspace(input_char()))
        input_next();
}

void input_skip_command
()
{
    input_skip_space();
    if (isdigit(input_char()))
    {
        while (isdigit(input_char()))
            input_next();
    }
    else
    {
        input_next();
    }    
}

long stack_nth
(int index)
{
    return stack_values[index];
}

void input_previous
()
{
    stream--;
}

/* Evaluate one character command */
void command_do
(char symbol)
{
    if (preserve > 0)
            preserve--;

    int a, b;
    a = 0;
    b = 0;
    switch (symbol)
    {
        case '+':;
            /* Dyadic addition */
            a = stack_pop();
            b = stack_pop();
            if (preserve) 
                stack_unpop(2);
            stack_push(a + b);
            break;
        case '-':;
            /* Dyadic subtraction */
            a = stack_pop();
            b = stack_pop();
            if (preserve) 
                stack_unpop(2);
            stack_push(b - a);
            break;
        case '*':;
            /* Dyadic multiplication */
            a = stack_pop();
            b = stack_pop();
            if (preserve) 
                stack_unpop(2);
            stack_push(a * b);
            break;
        case '/':;
            /* Dyadic division */
            a = stack_pop();
            b = stack_pop();
            if (preserve) 
                stack_unpop(2);
            stack_push(b / a);
            break;
        case '~':;
            /* Unary negation */
            a = -1 * stack_pop();
            if (preserve)
                stack_unpop(1);
            stack_push(a);
            break;
        case '"':
            /* Nilary pop the top of the stack */
            stack_pop();
            if (preserve) 
                stack_unpop(1);
            break;
        case '!':
            /* Unary pop the top of the stack */
            a = stack_pop();
            if (preserve)
                stack_unpop(1);
            for (b = 0; b < a; b++)
                stack_pop();
            /* There is no stack preservation for this last operation */
            break;
        case 'p':
            /* Unary print the top of the stack as a number */
            printf("%ld", stack_top());
            if (preserve)
                stack_unpop(1);
            break;
        case 'P':;
            /* Unary print the top of the stack as a character */
            a = stack_pop();
            if (preserve)
                stack_unpop(1);
            putchar((char) a);
            break;
        case '^':
            /* Nilary get a character and put it on the stack */
            stack_push((long) getchar());
            break;
        case '#':;
            /* Nilary read a number from stdin */
            char c = getchar();
            a = 0;
            while (isdigit(c))
            {
                a *= 10;
                a += decimal_value(c);
                c = getchar();
            }
            stack_push(a);
            break;
        case '?':
            /* Unary only use the next character if top of stack is true */
            if (stack_pop())
                input_skip_command();
            if (preserve) 
                stack_unpop(1);
            break;
        case '=':
            /* Dyadic compare for equality, preserving operands */
            a = stack_pop();
            b = stack_pop();
            if (preserve) 
                stack_unpop(2);
            stack_push(a == b);
            break;
        case '`':
            /* Unary logical not, N -> 0, 0 -> 1 */
            a = stack_pop();
            if (preserve) 
                stack_unpop(1);
            stack_push(!a);
            break;
        case '\'':
            /* Nilary push a string to the stack, delimited by 'single quotes' */
            input_next(); /* skip the first quote */
            stack_push('\0');
            while (input_char() && input_char() != '\'')
            {
                stack_push(input_char());
                input_next();
            }
            break;
        case 'S':;
            /* Nilary print, by popping the stack until a 0 is reached */
            a = 0; /* Keep track of how much to increment the stack if preserved */
            while (stack_top())
            {
                putchar(stack_pop());
                a++;
            }
            stack_pop(); /* remove the null terminator */
            if (preserve)
                stack_unpop(a+1);
            break;
        case '\\':
            /* Unary backslash to get the value of the next character */
            input_next(); /* Skip the '\' */
            stack_push((long) input_char());
            break;
        case ';':
            /* Nilary loop back to beginning */
            stream = input_buffer;
            break;
        case '$':
            /* Nilary preserve the operands for the next operation */
            /* Preserve starts out as 2 so that it will be reset after 1 additional loop */
            preserve = 2;
            break;
        case 'x':;
            /* Unary square a number */
            a = stack_pop();
            a *= a;
            if (preserve)
                stack_unpop(1);
            stack_push(a);
            break;
        case '.':
            /* Nilary duplicate the top of the stack */
            stack_push(stack_top());
            break;
        case '&':
            /* Unary evaluate the top of the stack */
            command_do(stack_pop());
            if (preserve)
                stack_unpop(1);
            break;
        case 'V':
            /* Peek at the Nth entry from the top of the stack */
            a = stack_pop();
            if (preserve)
                stack_unpop(1);
            stack_push(stack_peek(a));
            break;
        case 'N':
            /* Peek at the nth entry in the stack */
            a = stack_pop();
            if (preserve)
                stack_unpop(1);
            stack_push(stack_nth(a));
            break;
        case 'l':
            /* Emit newline / carriage return (equivalent to evaluating `10P') */
            putchar('\n');
            break;
        case 't':
            /* Emit a tab (equivalent to evaluating `9P') */
            putchar('\t');
            break;
        case 'H':
            /* Halve the top of the stack */
            a = stack_pop();
            if (preserve)
                stack_unpop(1);
            stack_push(a/2);
            break;
        case 'D':
            /* Double the top of the stack */
            a = stack_pop();
            if (preserve)
                stack_unpop(1);
            stack_push(a*2);
            break;
        case 'q':
            /* Square root of top of the stack */
            a = stack_pop();
            if (preserve)
                stack_unpop(1);
            stack_push((long) sqrt((double) a));
            break;
        case 'i':
            /* Increment the top of the stack */
            a = stack_pop();
            if (preserve)
                stack_unpop(1);
            stack_push(a + 1);
            break;
        case 'd':
            /* Decrement the top of the stack */
            a = stack_pop();
            if (preserve)
                stack_unpop(1);
            stack_push(a - 1);
            break;
        default:
            if (isdigit(symbol))
            {
                /* Push literal integer onto the stack */
                long n = 0;
                while (isdigit(input_char()))
                {
                    n *= 10;
                    n += decimal_value(input_char());
                    input_next();
                }
                input_previous();
                stack_push(n);
            }
            /* Any other character is skipped */
            break;
    }
}

int main
()
{
    fgets(input_buffer, INPUT_SIZE, stdin);
    stream = input_buffer;
    preserve = 0;
    
    while (input_char())
    {
        command_do(input_char());
        input_next();
    }
}

/*
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
*/