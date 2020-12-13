char hex_nibble (unsigned char c, int hi_low)
{
	char digits[] = "0123456789ABCDEF";
	int index = hi_low ? (c >> 4) : (c & 0x0F);
	assert((0 <= index) && (index <= 15));
	return digits[index];
}

char printable (char c)
{
	return ((31 < c) && (c < 127)) ? c : '.';
}

void hex_dump (char * mem, int length)
{
	int i, j;
	for (i = 0; i < (length / 16); i++)
	{
		printf("%p ", mem + (i * 16));
		for (j = 0; (j < 16) && ((i * 16 + j) < length); j++)
		{
			char c = mem[i * 16 + j];
			printf(" %c%c", hex_nibble(c, 1), hex_nibble(c, 0));
			if (((j+1) % 4) == 0)
			{
				putchar(' ');
			}
		}
		putchar(' ');
		for (j = 0; j < 16; j++)
		{
			char c = mem[i * 16 + j];
			printf("%c", printable(c));
		}
		putchar('\n');
	}
}

