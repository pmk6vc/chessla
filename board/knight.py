from typing import List, Tuple
from board.piece import Piece, Move


class Knight(Piece):
    def __init__(self, position: Tuple[int, int], is_white: bool):
        super().__init__(position, is_white)

    @property
    def label(self):
        return 'N'

    def move_options(self, board_state:List[Piece], move_list:List[str], attack_values:List[List[int]]) -> List[Move]:
        options = []
        occupied_squares_other_color = set(piece.position for piece in board_state if piece.is_white != self.is_white)
        occupied_squares = set(piece.position for piece in board_state)

        horizontal_offsets = [-2, -1, 1, 2]
        for horizontal_offset in horizontal_offsets:
            for vertical_offset in [int(2 / horizontal_offset), int(-2 / horizontal_offset)]:
                square = (self.position[0] + horizontal_offset, self.position[1] + vertical_offset)
                if square not in occupied_squares:
                    options.append(Move(
                        pieces_to_update=[self],
                        positions=[square]
                    ))
                elif square in occupied_squares_other_color:
                    captured_piece = next((piece for piece in board_state if piece.position == square))
                    options.append(Move(
                        pieces_to_update=[self, captured_piece],
                        positions=[square, (None, None)]
                    ))
        return options
