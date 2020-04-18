from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Tuple, Type


class Piece(ABC):
    def __init__(self, position:Tuple[int, int], is_white:bool):
        self._position = position
        self._is_white = is_white

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position:Tuple[int, int]):
        self._position = new_position

    @property
    def is_white(self):
        return self._is_white

    @abstractmethod
    def move_options(self, board_state:List[Type[Piece]], move_list:List[str]) -> List[Tuple[int, int]]:
        pass

    def move(self, new_position:Tuple[int, int], move_list:List[str]):
        self.position = new_position


class Pawn(Piece):
    def __init__(self, position:Tuple[int, int], is_white:bool):
        super().__init__(position, is_white)
        self.move_index = 0

    def in_default_position(self):
        return (self.is_white and self.position[1] == 1) or (~self.is_white and self.position[1] == 6)

    def move_options(self, board_state:List[Type[Piece]], move_list:List[str]) -> List[Tuple[int, int]]:
        """
        Enumerate four options:
        - Move one step forward to unoccupied square
        - Move two steps forward to unoccupied square if in starting square and path is unobstructed
        - Move diagonally one square if square is occupied by opponent piece
        - Move diagonally one square if neighboring square is occupied by pawn that moved two squares
        """
        options = []
        occupied_squares_other_color = set(piece.position for piece in board_state if piece.is_white != self.is_white)
        occupied_squares = set(piece.position for piece in board_state)
        next_square = (self.position[0], self.position[1] + 1 if self.is_white else self.position[1] - 1)
        double_square = (self.position[0], self.position[1] + 2 if self.is_white else self.position[1] - 2)
        left_capture_square = (self.position[0] - 1, self.position[1] + 1 if self.is_white else self.position[1] - 1)
        right_capture_square = (self.position[0] + 1, self.position[1] + 1 if self.is_white else self.position[1] - 1)
        left_neighbor_square = (self.position[0] - 1, self.position[1])
        right_neighbor_square = (self.position[0] + 1, self.position[1])
        # Move one step
        if next_square not in occupied_squares:
            options.append(next_square)
        # Move two steps if in starting position
        if self.in_default_position() and next_square not in occupied_squares and double_square not in occupied_squares:
            options.append(double_square)
        # Capture diagonally if populated by piece of other color
        if left_capture_square in occupied_squares_other_color:
            options.append(left_capture_square)
        if right_capture_square in occupied_squares_other_color:
            options.append(right_capture_square)
        # Capture en passant if neighboring square is populated by pawn that just moved two steps in the previous turn
        for piece in board_state:
            if isinstance(piece, Pawn) and piece.is_white != self.is_white and piece.move_index == len(move_list):
                if piece.position == left_neighbor_square:
                    options.append(left_neighbor_square)
                if piece.position == right_neighbor_square:
                    options.append(right_neighbor_square)
        return options

    def move(self, new_position:Tuple[int, int], move_list:List[str]):
        self.move_index = len(move_list)
        self.position = new_position
