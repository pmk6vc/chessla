from typing import List, Tuple, Type
from board.piece import Piece
from board.pawn import Pawn
from board.king import King
from board.knight import Knight
from board.bishop import Bishop
from board.rook import Rook
from board.queen import Queen


class BoardManager:
    def __init__(self):
        self._board_state = [Pawn(position=(x, 1), is_white=True) for x in range(8)] + \
            [King(position=(4, 0), is_white=True)] + \
            [Knight(position=(1, 0), is_white=True), Knight(position=(6, 0), is_white=True)] + \
            [Bishop(position=(2, 0), is_white=True), Bishop(position=(5, 0), is_white=True)] + \
            [Rook(position=(0, 0) ,is_white=True), Rook(position=(7, 0), is_white=True)]
        self.move_list = []

    @property
    def board_state(self):
        return [piece for piece in self._board_state if piece.position[0] is not None and piece.position[1] is not None]

    def retrieve_move_options(self) -> List[Tuple[int, int]]:
        # TODO: Check for discovered check and prune list here - can be done in each piece's class but want to avoid replicated code
        # TODO: Check for out of bounds
        for piece in self.board_state:
            for move in piece.move_options(self.board_state, self.move_list, self.retrieve_attack_values()):
                print(str(move))
        pass

    def retrieve_attack_values(self):
        # TODO
        return [[0 for col in range(7)] for row in range(7)]

    def move_piece(self):
        # Log move first
        # Execute move
        pass

    def is_legal(self, piece:Type[Piece], proposed_move:Tuple[int, int]) -> bool:
        pass