# yay! chess

### NOTE: This repository is not finished. I'll try making progress on finishing this whenever I have time between things.

This is a recreation of a simple but interesting chess engine I made in my junior year of college for a college presentation. It's named "yay!" because that's how I felt when I wrote my first chess engine. It's not nearly as powerful as the best chess engines in the world and I've learned a lot more since I first implemented the ideas in this chess engine, but it has some interesting algorithms that I found really interesting and loved implementing and talking about. This project would have been impossible without the [Chess Programming Wiki](https://chessprogramming.org). Feel free to use any of this code in your own engine for prototyping or for learning, it's MIT licensed.

Please make an issue if you see anything that may be inaccurate. Chess engines are just a hobby I enjoy exploring--so as an amateur, I might be wrong on some things.

All the comics in this README.md are by [xkcd.com.](https://xkcd.com) They make pretty good comics. For example, here's one:

<img src="xkcd/2936.png" width="500px">

> Karpov's construction of a series of increasingly large rice cookers led to a protracted deadlock, but exponential growth won in the end. - [#2936](https://xkcd.com/2936/)

If you want a reason for making your own chess engine, I'd argue it helped me personally learn how to get started in managing code with multiple moving parts that require good design to not mess up other parts of the code. For example, the choices you make in representing your board affects how fast your search is because there may be better move generation techniques for a specific board representation. It was also a way to apply some cool techniques I learnt in school that have applications in the real world, like bitmasking, hashing algorithms, search algorithms, reading challenging papers to implement ideas from academia, machine learning, good data structure design, and so much more.

The original is lost to time because I accidentally erased the copy while resetting my PC, but the good thing is that chess programming is a very neat topic that has good documentation and a sense of modularity. If you want a more in-depth explanation, visit the wiki linked above--the brillant and generous people who wrote it will be able to explain topics in much more accuracy and depth than I can. If you want a simple digest of chess engine anatomy for getting started, keep reading!

These are the three parts that make up this chess engine:

1. **Board Representation**: Computers only known binary encodings of things, how do we represent all the intricacies of a position--where the pieces are, if we can castle, who's move is it? More importantly, how do we make it efficient to store millions of these positions in working memory? How can we implement representations that make other parts of the chess engine easier, like generating moves or assigning scores to positions?

    - Also, how do we implement a way to iterate over all possible moves of a given position? This is called *move generation*.

2. **Search**: How do we search through all the different possible combinations of moves that make a chess game? How should we distribute the limited computing power we have to search these combinations?

3. **Evaluation**: What makes a chess position winning for one side? How do we assign scores to positions so we know which moves to suggest and which moves to ignore?

## Board Representation

> Prediction for Carlsen v. Anand: ... 25. Qb8+ Nxb8 26. Rd8# f6 27. "... dude." Qf5 28. "The game is over, dude." Qxg5 29. Rxe8 0-1 30. "Dude, your move can't be '0-1'. Don't write that down." [Black flips board] - [#1287](https://www.xkcd.com/1287/)

<img align="right" src="xkcd/1287.png">

As humans, experienced chess players learn and play the game visually on a 2D 
board. Computers don't work like that. Maybe they could, with some magical computer vision model (see [chessvision.ai](https://chessvision.ai)), but it's so much easier both computationally and implementation-wise to display a chess position as a 2D-array of possible pieces.

The yay! chess engine uses bitboards to achieve this, using the idea of having 12 8×8 2D boolean arrays--one for each of the 6 piece for each of the 2 sides--which indicates whether the side-and-piece class occupies a square for all the 8×8 squares on a chess board. However, instead of having 12 8×8 booleans arrays, we use the fact that an unsigned 64 bit integer has 64 bits, and can act like an array of booleans with some fancy operations that we use to manipulate individual bits for better optimization for CPU instructions such as the x86 BMI2 instruction set.

Below is an example of the black pawn bitboard from white's perspective at the starting chess position. Notice how the only 1 bits are on the row where the black pawns start.

```py
# Let binary(str) be a function that converts a string of 1's and 0's
# into a unsigned 64 bit integer
np.uint64(71776119061282560) == binary(
    "00000000"
    "11111111" # Black's army of pawns!
    "00000000"
    "00000000"
    "00000000" # It's all zeroes because
    "00000000" # black pawns don't occupy 
    "00000000" # these squares...
    "00000000"
)
```

Let's try making the bitboard for the white side's knights in the starting position:

```py
# Let binary(str) be a function that converts a string of 1's and 0's
# into a unsigned 64 bit integer
np.uint64(66) == binary(
    "00000000"
    "00000000"
    "00000000"
    "00000000" # The vast occupied 0's
    "00000000"
    "00000000"
    "00000000"
    "01000010" # Knights start at the first rank!
)
```

All of this might look needlessly complicated, but bitboards have some useful properties that allow us to generate moves rather efficiently. For example, what if we want to find all the squares that the white side occupies at the starting position?

```py
bitboards = \
    Let bitboards represent an unsigned 64-bit integer array
    of length 12, where the first 6 indices refer to the occupancies
    of the six white pieces.

# Initialize a zero unsigned 64-bit integer
white_occupancies = np.uint64(0)

# Find the bitwise OR of all the bitboards.
# In other words, if a 1-bit exists on any
# of the 6 piece bitboards for white, set the
# corresponding bit on the occupancy bitboard
# to from a 0-bit to a 1-bit.
for i in range(0, 6):
    white_occupancies |= bitboards[i]

print(white_occupancies) # Let's assume that this pretty-prints it as a binary number.
```

```
Output:
00000000
00000000
00000000
00000000
00000000
00000000
11111111
11111111
```

> In Dimensional Chess, every move is annotated '?!'. - [#2465](https://www.xkcd.com/2465)

<img src="xkcd/2465.png" align="right" width="330px">

With a naive 8×8 enumerated 2D-array approach, we'd need to iterate through all 64 bytes of a mailbox minimum due to alignment, and see if those bytes are in the range of our white piece enums. On the other hand, the bitboard approach leverages specific CPU instructions implemented at the low-level for the explicit purpose of making calculations fast like the aforementioned BMI2.

What about knights and king moves? On naive approaches, we'd need to dynamically calculate the indices for the moves that a knight can do. For a bitboard approach, we can initialize a array of unsigned 64-bit integers with a length of 64 on startup, where each index represents a square. A knight, when not blocked by any friendly pieces, can only make one set of moves for a given square. When we need to generate moves for a knight, just look up the square in the lookup table, calculate the bitwise AND between the lookup table and the negation of the friendly side's occupancy bitboard, and then extract the bits as possible moves for that given knight.

```py
white_occupancies = \
    Calculated above, can be re-used.
idx = \
    The row-times-column index where the white knight resides
knight_lookup = \
    Let white_knight_bitboard be the bitboard of white knights

moves = knight_lookup[idx] & ~white_occupancies
```

### Sliding Piece Move Generation: My Computer is Magical?!

Incomplete, but [this video](https://youtu.be/_vqlIPDR2TU?t=1714) explains the sliding piece move generation really well.