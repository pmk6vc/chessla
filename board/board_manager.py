import copy
from typing import List, Tuple, Type
from board.piece import Piece, Move
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
        self.is_white = True

    @property
    def board_state(self):
        return [piece for piece in self._board_state if piece.position[0] is not None and piece.position[1] is not None]

    def retrieve_all_moves(self, board_state:List[Piece], move_list:List[str]) -> List[Move]:
        """
        Retrieve all moves defined from each piece's move definition based on a given board state - will include possible illegal moves
        """
        candidate_moves = []
        for piece in board_state:
            candidate_moves += piece.move_options()

    def retrieve_possible_board_states(self, board_state:List[Piece], move_list:List[str]) -> List[List[Piece]]:
        # TODO: Check for discovered check and prune list here - can be done in each piece's class but want to avoid replicated code
        next_board_states = []
        # Retrieve all candidate moves based on current piece configuration
        attack_values = self.retrieve_attack_values(board_state)
        candidate_moves = []
        for piece in board_state:
            candidate_moves += piece.move_options(board_state, move_list, attack_values)

        # Execute each candidate move on a copy of this board state and determine whether execution results in illegal board state
        all_possible_moves = []
        for piece in board_state:
            all_possible_moves += piece.move_options(board_state, )

        for piece in board_state:
            for move in piece.move_options(board_state, move_list, attack_values):
                # Out of bounds
                out_of_bounds = False
                for position in move.positions:
                    if max(position) > 7 or min(position) < 0:
                        out_of_bounds = True
                # Retrieve King position to check whether it is under attack
                king_position = next((piece.position for piece in move.pieces_to_update if isinstance(piece, King)), None) or king_position

        pass

    def generate_new_board_state(self, board_state:List[Piece], move_list:List[str], move:Move) -> List[Piece]:


    def retrieve_attack_values(self, board_state:List[Piece]):
        # TODO
        return [[0 for col in range(7)] for row in range(7)]

    def move_piece(self):
        # Log move first
        # Execute move
        pass

    def is_legal(self, piece:Type[Piece], proposed_move:Tuple[int, int]) -> bool:
        pass