from typing import List, Tuple, Type
from board.pieces import Piece, Pawn


class BoardManager:
    def __init__(self):
        self.board_state = [Pawn(position=(x, 1), is_white=True) for x in range(8)] + \
            [Pawn(position=(x, 6), is_white=False) for x in range(8)]
        self.move_list = []

    def retrieve_move_options(self) -> List[Tuple[int, int]]:
        for piece in self.board_state:
            print(piece.position, piece.move_options(self.board_state, self.move_list))
        pass

    def move_piece(self):
        # self.move_list.append()
        pass

    def pawn_promotion(self):
        pass

    def is_legal(self, piece:Type[Piece], proposed_move:Tuple[int, int]) -> bool:
        pass