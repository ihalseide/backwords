# example code to convert to backwords for "print num.txt"

from sys import stdin, stdout

x = int(ord(stdin.read(1)))

if x > 0x63:
    if x > 0xc7:
        stdout.write('2')
        x -= 200
    else:
        stdout.write('1')
        x -= 100
else:
    stdout.write('0')

if x > 9:
    n = x // 10
    c = ord('0') + n
    stdout.write(chr(c))
    n *= 10
    x -= n
else:
    stdout.write('0')

stdout.write(chr(ord('0') + x))




