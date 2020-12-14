struct word_header {
	struct word_header * previous;
	cell name_len;
	char name [8];
	void (* code) (void);
}
