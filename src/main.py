"""
Entry point for the program. It immediately calls
the command line interface, which handles a language
called the Universal Chess Interface (UCI).
"""
import uci

if __name__ == "__main__":
    try:
        uci.init()
    except KeyboardInterrupt:
        None