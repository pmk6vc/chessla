from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional


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

    @property
    @abstractmethod
    def label(self):
        pass

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
        def map_position_to_suffix(position) -> str:
            return str(chr(ord('a') + position[0]) + str(position[1] + 1))
        return ', '.join([piece.label + map_position_to_suffix(piece.position) + '->' + map_position_to_suffix(position)
                          for piece, position in zip(self.pieces_to_update, self.positions)])
