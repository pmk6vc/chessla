from typing import List, Tuple, Set
from board.piece import Piece, Move


class Bishop(Piece):
    def __init__(self, position: Tuple[int, int], is_white: bool):
        super().__init__(position, is_white)

    def move_options(self, board_state:List[Piece], move_list:List[str], attack_values:List[List[int]]) -> List[Move]:
        options = []
        occupied_squares_other_color = set(piece.position for piece in board_state if piece.is_white != self.is_white)
        occupied_squares = set(piece.position for piece in board_state)

        # Northwest
        distance_to_edge = min(self.position[0], 7 - self.position[1])
        for offset in range(1, distance_to_edge + 1):
            square = (self.position[0] - 1, self.position[1] + 1)
            if square in occupied_squares_other_color:
                captured_piece = next((piece for piece in board_state if piece.position == square))
                options.append(Move(
                    pieces_to_update=[self, captured_piece],
                    positions=[square, (None, None)]
                ))
                break
            elif square in occupied_squares:
                break
            else:
                options.append(Move(
                    pieces_to_update=[self],
                    positions=[square]
                ))
        # Northeast
        distance_to_edge = min(7 - self.position[0], 7 - self.position[1])
        for offset in range(1, distance_to_edge + 1):
            square = (self.position[0] + 1, self.position[1] + 1)
            if square in occupied_squares_other_color:
                captured_piece = next((piece for piece in board_state if piece.position == square))
                options.append(Move(
                    pieces_to_update=[self, captured_piece],
                    positions=[square, (None, None)]
                ))
                break
            elif square in occupied_squares:
                break
            else:
                options.append(Move(
                    pieces_to_update=[self],
                    positions=[square]
                ))
        # Southeast
        distance_to_edge = min(7 - self.position[0], self.position[1])
        for offset in range(1, distance_to_edge + 1):
            square = (self.position[0] + 1, self.position[1] - 1)
            if square in occupied_squares_other_color:
                captured_piece = next((piece for piece in board_state if piece.position == square))
                options.append(Move(
                    pieces_to_update=[self, captured_piece],
                    positions=[square, (None, None)]
                ))
                break
            elif square in occupied_squares:
                break
            else:
                options.append(Move(
                    pieces_to_update=[self],
                    positions=[square]
                ))
        # Southwest
        distance_to_edge = min(self.position[0], self.position[1])
        for offset in range(1, distance_to_edge + 1):
            square = (self.position[0] - 1, self.position[1] - 1)
            if square in occupied_squares_other_color:
                captured_piece = next((piece for piece in board_state if piece.position == square))
                options.append(Move(
                    pieces_to_update=[self, captured_piece],
                    positions=[square, (None, None)]
                ))
                break
            elif square in occupied_squares:
                break
            else:
                options.append(Move(
                    pieces_to_update=[self],
                    positions=[square]
                ))
        return options
