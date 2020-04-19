from typing import List, Tuple, Set
from board.piece import Piece, Move
from board.rook import Rook


class King(Piece):
    def __init__(self, position:Tuple[int, int], is_white:bool):
        super().__init__(position, is_white)

    @property
    def label(self):
        return 'K'

    def consider_castle(self, board_state:List[Piece], attack_values:List[List[int]], occupied_squares:Set[Tuple[int, int]], move_options:List[Move],
                        required_rook_square:Tuple[int, int], squares_in_between:List[Tuple[int, int]], new_rook_square:Tuple[int, int], new_king_square:Tuple[int, int]):
        # If king has moved, do not castle
        if not self.in_default_position():
            return
        # If king is in check, do not castle
        if attack_values[self.position[0]][self.position[1]]:
            return
        # If squares in between castling are occupied or attacked, do not castle
        for square in squares_in_between:
            if square in occupied_squares or attack_values[square[0]][square[1]]:
                return
        # If king will end in check, do not castle
        if attack_values[new_king_square[0]][new_king_square[1]]:
            return
        # If rook has moved, do not castle
        required_rook = next((piece for piece in board_state if piece.position == required_rook_square), None)
        if not isinstance(required_rook, Rook) or ~required_rook.in_default_position():
            return
        move_options.append(Move(
            pieces_to_update=[self, required_rook],
            positions=[new_king_square, new_rook_square]
        ))

    def move_options(self, board_state:List[Piece], move_list:List[str], attack_values:List[List[int]]) -> List[Move]:
        options = []
        occupied_squares_same_color = set(piece.position for piece in board_state if piece.is_white == self.is_white)
        occupied_squares = set(piece.position for piece in board_state)

        # Move to immediate neighboring squares
        for horizontal_offset in range(-1, 2):
            for vertical_offset in range(-1, 2):
                if horizontal_offset == vertical_offset == 0:
                    continue
                square = (self.position[0] + horizontal_offset, self.position[1] + vertical_offset)
                if square not in occupied_squares_same_color:
                    if square in occupied_squares:
                        captured_piece = next((piece for piece in board_state if piece.position == square))
                        options.append(Move(
                            pieces_to_update=[self, captured_piece],
                            positions=[square, (None, None)]
                        ))
                    else:
                        options.append(Move(
                            pieces_to_update=[self],
                            positions=[square]
                        ))
        # Castling
        if self.is_white:
            self.consider_castle(
                board_state=board_state,
                attack_values=attack_values,
                occupied_squares=occupied_squares,
                move_options=options,
                required_rook_square=(7, 0),
                squares_in_between=[(5, 0), (6, 0)],
                new_rook_square=(5, 0),
                new_king_square=(6, 0)
            )
            self.consider_castle(
                board_state=board_state,
                attack_values=attack_values,
                occupied_squares=occupied_squares,
                move_options=options,
                required_rook_square=(0, 0),
                squares_in_between=[(1, 0), (2, 0), (3, 0)],
                new_rook_square=(3, 0),
                new_king_square=(2, 0)
            )
        else:
            self.consider_castle(
                board_state=board_state,
                attack_values=attack_values,
                occupied_squares=occupied_squares,
                move_options=options,
                required_rook_square=(7, 7),
                squares_in_between=[(5, 7), (6, 7)],
                new_rook_square=(5, 7),
                new_king_square=(6, 7)
            )
            self.consider_castle(
                board_state=board_state,
                attack_values=attack_values,
                occupied_squares=occupied_squares,
                move_options=options,
                required_rook_square=(0, 7),
                squares_in_between=[(1, 7), (2, 7), (3, 7)],
                new_rook_square=(3, 7),
                new_king_square=(2, 7)
            )
        return options