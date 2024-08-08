from enum import Enum, Flag

class Piece(Enum):
    WHITE_KING = 0,
    WHITE_QUEEN = 1,
    WHITE_ROOK = 2,
    WHITE_KNIGHT = 3,
    WHITE_BISHOP = 4,
    WHITE_PAWN = 5,
    BLACK_KING = 6,
    BLACK_QUEEN = 7,
    BLACK_ROOK = 8,
    BLACK_KNIGHT = 9,
    BLACK_BISHOP = 10,
    BLACK_PAWN = 11,
    NULL_PIECE = 12,

class Side(Flag):
    WHITE = 0,
    BLACK = 1,