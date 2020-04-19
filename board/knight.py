from typing import Tuple
from board.pieces import Piece


class Knight(Piece):
    def __init__(self, position: Tuple[int, int], is_white: bool):
        super().__init__(position, is_white)