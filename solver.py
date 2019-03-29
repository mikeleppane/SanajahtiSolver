#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import copy
import sys
from collections import OrderedDict, deque
from operator import mul


class Solver(object):
    def __init__(self):
        self.game_attributes = Attributes()
        self.game_board = GameBoard()

    def start_solver(self, characters, size):
        self.game_board = GameBoard.create_game_board(characters, size)
        for row in self.game_board.rows:
            for column in self.game_board.columns:
                self.game_attributes.visited_nodes.append(
                    self.game_board.game_board[row, column])
                self._solve_neighbouring_nodes(row, column)
                self.game_attributes.visited_nodes.clear()

    def _solve_neighbouring_nodes(self, row, column):
        for index in self.get_neighbour_indexes(row, column):
            if (0 <= index[0] < len(self.game_board.rows) and
                    0 <= index[1] < len(self.game_board.columns)) and \
                    self.game_board.game_board[index] not in self.game_attributes.visited_nodes:
                self.game_attributes.visited_nodes.append(
                    self.game_board.game_board[index])
                if self._is_valid_word(self._get_word()):
                    self._solve_neighbouring_nodes(index[0], index[1])
                else:
                    self.game_attributes.visited_nodes.pop()
        self.game_attributes.visited_nodes.pop()
        return

    @staticmethod
    def get_neighbour_indexes(row, column):
        return [(row - 1, column - 1), (row - 1, column),
                (row - 1, column + 1), (row, column - 1),
                (row, column + 1), (row + 1, column - 1),
                (row + 1, column), (row + 1, column + 1)]

    def _get_word(self):
        return "".join((node[2]
                        for node in self.game_attributes.visited_nodes))

    def _is_valid_word(self, word):
        if len(word) > 1:
            if self._contains(word):
                if word in self.game_attributes.set_of_valid_words:
                    self.game_attributes.found_words.update({
                        word:
                        copy.deepcopy(self.game_attributes.visited_nodes)
                    })
                return True
        return False

    def _contains(self, value):
        index = self._bisect_left(value)
        return index < len(
            self.game_attributes.list_of_valid_words_sorted
        ) and self.game_attributes.list_of_valid_words_sorted[index].startswith(value)

    def _bisect_left(self, value):
        left, right = 0, len(self.game_attributes.list_of_valid_words_sorted)
        while left < right:
            middle = (left + right) // 2
            if self.game_attributes.list_of_valid_words_sorted[middle][:len(
                    value)] < value:
                left = middle + 1
            else:
                right = middle
        return left


class Attributes(object):
    visited_nodes = deque()
    words = set()
    set_of_valid_words = set()
    list_of_valid_words_sorted = list()
    found_words = dict()


class GameBoard(object):
    game_board = OrderedDict()
    rows = range(0)
    columns = range(0)

    @classmethod
    def create_game_board(cls, characters, board_size):
        if not isinstance(board_size, tuple):
            raise TypeError("Given size must a type of tuple")
        if isinstance(characters, str):
            if len(characters) != mul(*board_size):
                raise IndexError(
                    "Given character string and size does not match!")
            cls.rows = range(0, board_size[0])
            cls.columns = range(0, board_size[1])
            start_index = 0
            for row in cls.rows:
                for column in cls.columns:
                    cls.game_board[(row,
                                    column)] = (row, column,
                                                characters[start_index])
                    start_index += 1
            return cls()
        raise TypeError("Given characters must a type of str")


class Parser(object):
    @staticmethod
    def extract_words_from_file(_file):
        if not _file:
            _file = "words.txt"
        with open(_file, 'r') as f:
            for line in f:
                Attributes.set_of_valid_words.add(line.strip())

        Attributes.list_of_valid_words_sorted = sorted(
            list(Attributes.set_of_valid_words))


def handle_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--characters", type=str, help="characters used in game board")
    parser.add_argument(
        "-s",
        "--size",
        type=int,
        default=2,
        help="the size of the game board [default: 2x2]")
    parser.add_argument(
        "-w",
        "--words",
        type=str,
        default=None,
        help="the path for words file in xml format")
    args = parser.parse_args()
    return args.characters, args.size, args.words


def print_results(found_words):
    print()
    for word in sorted(found_words.keys(), key=len, reverse=True):
        visited_nodes = found_words[word]
        print("Found word: {}, ".format(word.upper()), end='')
        print("Word path: ", end='')
        for i, node in enumerate(visited_nodes, start=1):
            if i == len(visited_nodes):
                print("({}, {})".format(node[0], node[1]), end='')
            else:
                print("({}, {}) -> ".format(node[0], node[1]), end='')
        print()


def main():
    chars, board_size, words_file = handle_commandline()
    Parser.extract_words_from_file(words_file)
    solver = Solver()
    solver.start_solver(chars, (board_size, board_size))
    print_results(solver.game_attributes.found_words)


if __name__ == '__main__':
    sys.exit(main())
