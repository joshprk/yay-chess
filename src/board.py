from calendar import c
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


@dataclass
class FromMoveStr:
    from_idx: int
    to_idx: int
    promotion: Piece


class Board:
    bitboards: np.array[np.uint64]
    side_to_move: Side
    castling: CastlingRights
    ep_state: int
    halfmove: int
    fullmove: int
    
    def __init__(self, fen: str | Iterator[Match[str]] = START_FEN):
        if type(fen) is str:
            fen = re.finditer(r"\S+", fen)
        elif type(fen) is not Iterator[Match[str]]:
            raise Exception("Invalid FEN type")

        self.bitboards = self.parse_board(next(fen).string)
        self.side_to_move = Side.WHITE if next(fen).string == "w" else Side.BLACK
        self.castling = self.parse_castling(next(fen).string)
        
        ep_str = next(fen).string
        self.ep_state = -1 if ep_str == "-" else (ord(ep_str[0].lower()) - ord('a')) + int(ep_str[1]) * 8
        self.halfmove = int(next(fen).string)
        self.fullmove = int(next(fen).string)

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


def parse_move(move: str) -> FromMoveStr:
    if move == "0000":
        return FromMoveStr(-1, -1, Piece.NULL_PIECE)

    from_x = ord(move[0].lower()) - ord('a')
    from_y = int(move[1])
    to_x = ord(move[2].lower()) - ord('a')
    to_y = int(move[3])

    from_idx = from_x + from_y * 8
    to_idx = to_x + to_y * 8
    promotion = Piece.NULL_PIECE

    if len(move) > 4:
        match move[4]:
            case "Q":
                promotion = Piece.WHITE_QUEEN
            case "R":
                promotion = Piece.WHITE_ROOK
            case "N":
                promotion = Piece.WHITE_KNIGHT
            case "B":
                promotion = Piece.WHITE_BISHOP
            case "q":
                promotion = Piece.BLACK_QUEEN
            case "r":
                promotion = Piece.BLACK_ROOK
            case "n":
                promotion = Piece.BLACK_KNIGHT
            case "b":
                promotion = Piece.BLACK_BISHOP
            case _:
                raise Exception("malformed movestr")

    return FromMoveStr(from_idx, to_idx, promotion)
