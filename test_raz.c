#include "raz.c"

#define K * 1024

void test_str_eq ()
{
	char * s1 = "superstring";
	char * s2 = "superstring";
	char * s3 = "sum dum";
	char * s4 = s1;
	for (int i = 0; i <= 11; i++)
	{
		assert(str_eq_(s1, i, s2, i));
	}
	// S1 == S3 for the first 2 chars
	for (int i = 0; i <= 2; i++)
	{
		assert(str_eq_(s1, i, s3, i));
	}
	// S2 == S3 for the first 2 chars
	for (int i = 0; i <= 2; i++)
	{
		assert(str_eq_(s2, i, s3, i));
	}
	// S1 != S3 for chars 3 and up
	for (int i = 3; i <= 7; i++)
	{
		assert(!str_eq_(s1, i, s3, i));
	}
	// S2 != S3 for chars 3 and up
	for (int i = 3; i <= 7; i++)
	{
		assert(!str_eq_(s2, i, s3, i));
	}
}

// Stack pushing and popping Test
void test_stacks ()
{
	cell x = 12;
	cell y = 64;

	assert(i_pstack == 0);
	push(x);
	assert(i_pstack == 1);
	assert(pstack[i_pstack - 1] == x);
	assert(x == pop());
	assert(i_pstack == 0);
	push(x);
	push(y);
	assert(y == pop());
	assert(x == pop());
	assert(i_pstack == 0);
}

void main ()
{
	printf("Dumping memory\n");
	hex_dump(memory, 2 K);

	printf("Dumping memory\n");
	hex_dump(memory, 2 K);

	printf("Testing stacks\n");
	test_stacks();

	printf("Testing string equality\n");
	test_str_eq();
}
