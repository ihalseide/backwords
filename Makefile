run: compile
	./raz.exe

compile_debug: raz.c
	gcc -std=c99 -Wall -o raz.exe raz.c -DDEBUG

compile: raz.c
	gcc -std=c99 -Wall -o raz.exe raz.c

debug: compile_debug
	gdb raz.exe

clean:
	rm raz.exe
