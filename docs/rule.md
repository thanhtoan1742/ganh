# Ganh

## Rule

A 2 player game.

### Board

4*4 squares with 25 intersection.
![initial position](docs/ganh_initial.jpg)

### Piece

Each player has 16 pieces.
The initial position is the layed out as above.

### Move

A piece can move along the edges specified on the board to an empty
intersection.

#### Carry

A piece move into an intersection between 2 opponent's pieces and form a line
with those 2 pieces -> turn those 2 pieces to yours.

#### Surround

Surround the opponent's pieces in a way that they can't be moved -> turn those
pieces to yours.

#### Open

If you moves your piece and the opponent has a chance to carry by moving to
initial position of the piece you moved, your opponent has to carry by moving
their piece to that position.
