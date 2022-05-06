############################################
# A simple game of checkers by Ndymario#2326
############################################

class Checker():
    def __init__(self, color, pos, is_king) -> None:
        self.color = color
        self.pos = pos
        self.is_king = is_king

# Standard size is 8x8
class CheckerBoard():
    def __init__(self, width = 8, height = 8) -> None:
        self.width = width
        self.height = height
        self.pieces = []

    def add_piece(self, piece):
        self.pieces.append(piece)

    def remove_piece(self, piece):
        self.pieces.remove(piece)

class CheckerGame():
    def __init__(self, width = 8, height = 8) -> None:
        self.board = self.create_game(width=width, height=height)

    def create_game(self, width, height):
        return CheckerBoard(width=width, height=height)