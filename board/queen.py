from typing import Tuple
from board.piece import Piece


class Queen(Piece):
    def __init__(self, position: Tuple[int, int], is_white: bool):
        super().__init__(position, is_white)

    @property
    def label(self):
        return 'Q'