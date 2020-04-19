from typing import List, Tuple, Optional
from board.piece import Piece, Move
from board.bishop import Bishop
from board.knight import Knight
from board.rook import Rook
from board.queen import Queen


class Pawn(Piece):
    def __init__(self, position:Tuple[Optional[int], Optional[int]], is_white:bool):
        super().__init__(position, is_white)

    @property
    def label(self):
        return ''

    def move_options(self, board_state:List[Piece], move_list:List[str], attack_values:List[List[int]]) -> List[Move]:
        options = []
        occupied_squares_other_color = set(piece.position for piece in board_state if piece.is_white != self.is_white)
        occupied_squares = set(piece.position for piece in board_state)

        next_square = (self.position[0], self.position[1] + 1 if self.is_white else self.position[1] - 1)
        double_square = (self.position[0], self.position[1] + 2 if self.is_white else self.position[1] - 2)
        left_capture_square = (self.position[0] - 1, self.position[1] + 1 if self.is_white else self.position[1] - 1)
        right_capture_square = (self.position[0] + 1, self.position[1] + 1 if self.is_white else self.position[1] - 1)
        left_neighbor_square = (self.position[0] - 1, self.position[1])
        right_neighbor_square = (self.position[0] + 1, self.position[1])

        # Move one step (including pawn promotion)
        if next_square not in occupied_squares:
            if (self.is_white and next_square[1] == 7) or (~self.is_white and next_square[1] == 0):
                options.append(Move(
                    pieces_to_update=[self, Knight(position=next_square, is_white=self.is_white)],
                    positions=[(None, None), next_square]
                ))
                options.append(Move(
                    pieces_to_update=[self, Bishop(position=next_square, is_white=self.is_white)],
                    positions=[(None, None), next_square]
                ))
                options.append(Move(
                    pieces_to_update=[self, Rook(position=next_square, is_white=self.is_white)],
                    positions=[(None, None), next_square]
                ))
                options.append(Move(
                    pieces_to_update=[self, Queen(position=next_square, is_white=self.is_white)],
                    positions=[(None, None), next_square]
                ))
            else:
                options.append(Move(
                    pieces_to_update=[self],
                    positions=[next_square]
                ))
        # Move two steps if in starting position
        if self.in_default_position() and next_square not in occupied_squares and double_square not in occupied_squares:
            options.append(Move(
                pieces_to_update=[self],
                positions=[double_square]
            ))
        # Capture diagonally if populated by piece of other color
        if left_capture_square in occupied_squares_other_color:
            captured_piece = next((piece for piece in board_state if piece.position == left_capture_square))
            options.append(Move(
                pieces_to_update=[self, captured_piece],
                positions=[left_capture_square, (None, None)]
            ))
        if right_capture_square in occupied_squares_other_color:
            captured_piece = next((piece for piece in board_state if piece.position == right_capture_square))
            options.append(Move(
                pieces_to_update=[self, captured_piece],
                positions=[right_capture_square, (None, None)]
            ))
        # Capture en passant and move to capture square if neighboring square is populated by pawn that just moved two steps in the previous turn
        for piece in board_state:
            if isinstance(piece, Pawn) and piece.is_white != self.is_white and piece.last_move_index == len(move_list):
                if piece.position == left_neighbor_square:
                    options.append(Move(
                        pieces_to_update=[self, piece],
                        positions=[left_capture_square, (None, None)]
                    ))
                if piece.position == right_neighbor_square:
                    options.append(Move(
                        pieces_to_update=[self, piece],
                        positions=[right_capture_square, (None, None)]
                    ))
        return options