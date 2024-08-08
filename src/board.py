from dataclasses import dataclass
from enum import Enum, Flag
from typing import Iterator
from re import Match
import re
import numpy as np

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Piece(Enum):
    WHITE_KING = (0,)
    WHITE_QUEEN = (1,)
    WHITE_ROOK = (2,)
    WHITE_KNIGHT = (3,)
    WHITE_BISHOP = (4,)
    WHITE_PAWN = (5,)
    BLACK_KING = (6,)
    BLACK_QUEEN = (7,)
    BLACK_ROOK = (8,)
    BLACK_KNIGHT = (9,)
    BLACK_BISHOP = (10,)
    BLACK_PAWN = (11,)
    NULL_PIECE = (12,)


class Side(Flag):
    WHITE = (0,)
    BLACK = (1,)

@dataclass
class CastlingRights:
    white_king: bool
    white_queen: bool
    black_king: bool
    black_queen: bool


class Board:
    bitboards: np.array[np.uint64]
    side_to_move: Side

    def __init__(self, fen: str | Iterator[Match[str]] = START_FEN):
        if type(fen) is str:
            fen = re.finditer(r"\S+", fen)
        elif type(fen) is not Iterator[Match[str]]:
            raise Exception("Invalid FEN type")

        self.bitboards = self.parse_board(next(fen))
        self.side_to_move = Side.WHITE if next(fen) == "w" else Side.BLACK

    def parse_board(board: str) -> np.array[np.uint64]:
        bitboards = np.array([0 for _ in range(64)], dtype=np.uint64)

        idx = 0
        for c in board:
            if not idx < 64:
                raise Exception("Board fen has too many characters")

            match c:
                case "/":
                    continue
                case "K":
                    bitboards[Piece.WHITE_KING] |= 1 << idx
                case "Q":
                    bitboards[Piece.WHITE_QUEEN] |= 1 << idx
                case "R":
                    bitboards[Piece.WHITE_ROOK] |= 1 << idx
                case "N":
                    bitboards[Piece.WHITE_KNIGHT] |= 1 << idx
                case "B":
                    bitboards[Piece.WHITE_BISHOP] |= 1 << idx
                case "P":
                    bitboards[Piece.WHITE_PAWN] |= 1 << idx
                case "k":
                    bitboards[Piece.BLACK_KING] |= 1 << idx
                case "q":
                    bitboards[Piece.BLACK_QUEEN] |= 1 << idx
                case "r":
                    bitboards[Piece.BLACK_ROOK] |= 1 << idx
                case "n":
                    bitboards[Piece.BLACK_KNIGHT] |= 1 << idx
                case "b":
                    bitboards[Piece.BLACK_BISHOP] |= 1 << idx
                case "p":
                    bitboards[Piece.BLACK_BISHOP] |= 1 << idx
                case c.isdigit():
                    if not 0 < int(c) <= 8:
                        raise Exception("A digit in the board fen is not in range")
                    idx += c
                case _:
                    raise Exception("Malformed board fen")

        return bitboards

    def parse_castling(castles: str) -> CastlingRights:
        rights = CastlingRights(False, False, False, False)

        for c in castles:
            match c:
                case "-":
                    return rights
                case "K":
                    rights.white_king = True
                case "Q":
                    rights.white_queen = True
                case "k":
                    rights.black_king = True
                case "q":
                    rights.black_queen = True
                case _:
                    raise Exception("Malformed castling rights")

        return rights
    
    