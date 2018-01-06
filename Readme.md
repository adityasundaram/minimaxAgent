This is an implementation of a game playing agent that is based on the minimax algorithm with alpha-beta pruning. 
There are some sample inputs which represents how the board is input to the program and the outputs represent the
valid move with gravity applied.

For example : 
K21  // refers to the position of the move where it started. Kth column, 21st row.
************************
************************
************************
*1**1*******************
*0**0**********0********
*1**1**0*******1********
*1**0**10******1**1*****
*1**0*011****1*01*1*****
*0**1*100****0*00*0****0
100*1*011****1*00*0****1
101*111101***1100*0****1
0010011111***1000*10***0
0010001100***1001*00***0
000010011101*01101000*00
110100111110*11010001001
111001000110*01110000010
101001011011001101000000
010001011111000100101000
101001111011111111010100
101011110000011100101011
100010111100100001000010
010000111111010110011011
110110110111110100011011
011011101100111110010100

The different digits on the board represent the fruits. This game is analogous to candy crush game. This game was written
in a way that the output can act as a perfect input to another gameplaying agent.
