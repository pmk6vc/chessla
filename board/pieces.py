from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Set


class Piece(ABC):
    def __init__(self, position:Tuple[Optional[int], Optional[int]], is_white:bool):
        self._position = position
        self._is_white = is_white
        self._last_move_index = 0

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position:Tuple[Optional[int], Optional[int]]):
        self._position = new_position

    @property
    def is_white(self):
        return self._is_white

    @property
    def last_move_index(self):
        return self._last_move_index

    @last_move_index.setter
    def last_move_index(self, move_list_length:int):
        self._last_move_index = move_list_length

    def in_default_position(self):
        return ~self.last_move_index

    @abstractmethod
    def move_options(self, board_state:List[Piece], move_list:List[str], attack_values:List[List[int]]) -> List[Move]:
        pass


class Move:
    def __init__(self, pieces_to_update:List[Piece], positions:List[Tuple[Optional[int], Optional[int]]]):
        self.pieces_to_update = pieces_to_update
        self.positions = positions

    def move(self, move_list:List[str]):
        move_list.append(str(self))
        for piece, position in zip(self.pieces_to_update, self.positions):
            piece.position = position
            piece.last_move_index = len(move_list)

    def __str__(self):
        def map_piece_to_prefix(piece):
            if isinstance(piece, Pawn):
                return ''
            elif isinstance(piece, Knight):
                return 'N'
            elif isinstance(piece, Bishop):
                return 'B'
            elif isinstance(piece, Rook):
                return 'R'
            elif isinstance(piece, Queen):
                return 'Q'
            elif isinstance(piece, King):
                return 'K'
        def map_position_to_suffix(position):
            return chr(ord('a') + position[0]) + str(position[1] + 1)
        return ', '.join([map_piece_to_prefix(piece) + map_position_to_suffix(piece.position) + '->' + map_position_to_suffix(position)
                          for piece, position in zip(self.pieces_to_update, self.positions)])


class Pawn(Piece):
    def __init__(self, position:Tuple[Optional[int], Optional[int]], is_white:bool):
        super().__init__(position, is_white)

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


class King(Piece):
    def __init__(self, position:Tuple[int, int], is_white:bool):
        super().__init__(position, is_white)

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


class Knight(Piece):
    def __init__(self, position: Tuple[int, int], is_white: bool):
        super().__init__(position, is_white)


class Bishop(Piece):
    def __init__(self, position: Tuple[int, int], is_white: bool):
        super().__init__(position, is_white)


class Rook(Piece):
    def __init__(self, position: Tuple[int, int], is_white: bool):
        super().__init__(position, is_white)

    def move_options(self, board_state:List[Piece], move_list:List[str], attack_values:List[List[int]]) -> List[Move]:
        return []


class Queen(Piece):
    def __init__(self, position: Tuple[int, int], is_white: bool):
        super().__init__(position, is_white)
