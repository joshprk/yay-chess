from typing import List
from position import Piece, parse_move
from state import State
import numpy as np

"""
This is the main event loop for the chess engine.

Chess engines use a language called the UCI
specification to communicate with each other. Some of
these commands aren't used anymore, but certain commands
are essential like "position" and "go". See the TXT file
linked below to get specific details about these commands.

https://github.com/joshprk/yay-chess/blob/main/uci.txt
"""


def init():
    # The object that contains all the relevant data on
    # a search for chess move from a given position to
    # start searching from.
    #
    # For more information, check out the Search chapter
    # on the README.md.
    state = State()

    while True:
        tokens = input().split()
        cmd = None

        try:
            cmd = tokens.pop(0)
        except IndexError:
            continue

        match cmd:
            case "uci":
                print("id name yay")
                print("id author joshprk")
                print("uciok")
            case "isready":
                print("readyok")
            case "position":
                state = position(tokens)
            case "go":
                go(tokens)
            case "stop":
                """"""
            case "test":
                test(tokens, state)
            case "quit":
                return
            case _:
                continue


def position(tokens: List[str]) -> State:
    idx = None
    try:
        idx = tokens.index("moves")
        state = State(" ".join(tokens[:idx]))
        tokens = tokens[idx+1:]

        while len(tokens) > 0:
            move = parse_move(tokens.pop(0))
            print(move)
            # state.position = state.position.make(move)

        return state
    except ValueError:
        return State(" ".join(tokens))

def go(tokens: List[str]):
    """"""

def test(tokens: List[str], state: State):
    cmd = None

    try:
        cmd = tokens.pop(0)
    except IndexError:
        return

    match cmd:
        case "pos":
            def get_piece_at_idx(idx: np.uint64) -> Piece:
                for p in range(len(state.position.bitboards)):
                    if (state.position.bitboards[p] >> idx) & np.uint64(1):
                        return Piece(p)
                
                return Piece.NULL_PIECE
                    
            def get_char_for_piece(p: Piece) -> str:
                match p:
                    case Piece.WHITE_KING:
                        return "K"
                    case Piece.WHITE_QUEEN:
                        return "Q"
                    case Piece.WHITE_ROOK:
                        return "R"
                    case Piece.WHITE_KNIGHT:
                        return "N"
                    case Piece.WHITE_BISHOP:
                        return "B"
                    case Piece.WHITE_PAWN:
                        return "P"
                    case Piece.BLACK_KING:
                        return "k"
                    case Piece.BLACK_QUEEN:
                        return "q"
                    case Piece.BLACK_ROOK:
                        return "r"
                    case Piece.BLACK_KNIGHT:
                        return "n"
                    case Piece.BLACK_BISHOP:
                        return "b"
                    case Piece.BLACK_PAWN:
                        return "p"
                    case _:
                        return "-"

            for y in range(8):
                print("|", end = " ")
                for x in range(8):
                    p = get_piece_at_idx(np.uint64(x + y * 8))
                    print(get_char_for_piece(p), end=" ")

                print("|", end="\n")
        case _:
            print("# unknown test command")