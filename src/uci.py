from typing import Iterator
from re import Match
from search import Search
import re

"""
This is the main event loop for the chess engine.

Chess engines use a language called the UCI
specification to communicate with each other. Some of
these commands aren't used anymore, but certain commands
are essential like "position" and "go". See the TXT file
linked below to get specific details about these commands.

https://github.com/joshprk/yay-chess/blob/main/uci.txt

The reason why I call it a language is because the easiest way 
to process these commands (which come from standard input) is
by making a parser which can understand the equivalent
grammar. Each token is separated by ASCII whitespace, and
for the parser to work, it needs to properly handle the
many but tractable possible combinations of tokens.
"""


def init():
    # The object that contains all the relevant data on
    # a search for chess move from a given position to
    # start searching from.
    #
    # For more information, check out the Search chapter
    # on the README.md.

    while True:
        tokens = re.finditer(r"\S+", input())
        match next(tokens, None).string:
            case "uci":
                print("id name yay")
                print("id author joshprk")
                print("uciok")
            case "isready":
                print("readyok")
            case "position":
                position(tokens)
            case "go":
                go(tokens)
            case "stop":
                """"""
            case "quit":
                return
            case _:
                continue


def position(tokens: Iterator[Match[str]]):
    """"""


def go(tokens: Iterator[Match[str]]):
    """"""
