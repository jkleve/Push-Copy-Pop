# Push-Copy-Pop
Push, copy, pop files in the terminal using a stack.

If you try this utility out, note that there is a global variable at the top of pcp.py called 'test' that when set to True will not perform the file operations. It will simply print to the console what it would do. Setting this to False will perform the file copy, moves, and deletes.

PCP uses a file in /tmp to keep track of the file stack. This allows you to jump from one terminal to another to perform push, pops. etc. 

I would suggest creating a symbolic link to pcp.py called pcp in a directory that is in your path. I have not taken the time yet to create an install script to do this for you.

I am open to anyone who wants to make suggestions or contribute.

contact: jesse.kleve@gmail.com
