from typing import List
from position import START_FEN, Position


class State:
    position: Position

    def __init__(self, fen: str | List[str] = START_FEN):
        if type(fen) is str:
            if fen == "startpos":
                fen = START_FEN
            fen = fen.split()

        self.position = Position(fen)