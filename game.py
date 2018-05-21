from btree import *
from board import Board

class WrongTurnError(Exception):
    pass


class Game:

    def __init__(self):
        self._board = Board()

    def turn(self, player, coord):
        i, j = coord
        self._board[i, j] = player

    def cur_position(self):
        return self._board

    def start_game(self):
        print('Game started')
        print(self._board)
        while not (self._board.check_winner() or self._board.is_filled()):
            self.make_turn()
            print('You: ')
            print(self._board)
            print('-' * 7)
            if self._board.check_winner() or self._board.is_filled():
                break
            self.handle_turn()
            print('Computer: ')
            print(self._board)
            print('-'* 7)
        if not self._board.check_winner():
            print('Draw')
        elif self._board.check_winner() == 'o':
            print('You won')
        else:
            print('Computer won')

    def _validate_turn(self, coord):
        coord = coord.split()
        if len(coord) != 2:
            raise WrongTurnError
        x, y = coord
        x = int(x)
        y = int(y)
        is_possible = lambda x: x >= 0 and x < 3
        if not is_possible(x) or not is_possible(y):
            raise WrongTurnError
        if self._board[x, y] is not None:
            raise WrongTurnError
        return True

    def make_turn(self):
        """Makes a turn by coordinates inputted by a person"""
        coord = input('Please, enter 2 coordinates, separated by space: ')
        try:
            if self._validate_turn(coord):
                coord = coord.split()
                x, y = coord
                x = int(x)
                y = int(y)
                if self._board[x, y] is not None:
                    raise WrongTurnError
                self._board[x, y] = 'o'
        except WrongTurnError:
            self.make_turn()

    def computer_turn(self, turn):
        self._board[turn[0], turn[1]] = 'x'

    def handle_turn(self):
        turn = self.choose_turn()
        self.computer_turn(turn)

    def make_decision_tree(self):
        root = self._board
        tree = LinkedBinaryTree(root)
        def another(player):
            if player == 'x':
                return 'o'
            elif player == 'o':
                return 'x'

        def make_board(board, turn, player):
            result = board.copy()
            i, j = turn
            result[i, j] = player
            return result

        def fork_from_root(tree, cur_pl):
            left, right = tree.get_root_val().random_possible_turns()
            if left is not None and right is not None:
                left_board = make_board(tree.get_root_val(), left, cur_pl)
                right_board = make_board(tree.get_root_val(), right, cur_pl)
                tree.insert_left(left_board)
                tree.insert_right(right_board)
                if not left_board.check_winner():
                    fork_from_root(tree.get_left_child(), another(cur_pl))
                if not right_board.check_winner():
                    fork_from_root(tree.get_right_child(), another(cur_pl))
            elif left is None and right is None:
                pass
            else:
                left_board = make_board(tree.get_root_val(), left, cur_pl)
                tree.insert_left(left_board)
                if not left_board.check_winner():
                    fork_from_root(tree.get_left_child(), another(cur_pl))
        fork_from_root(tree, 'x')
        return tree

    def choose_turn(self):
        choice_tree = self.make_decision_tree()
        variant1 = choice_tree.get_left_child()
        variant2 = choice_tree.get_right_child()
        def find_points(variant):
            if variant:
                possibilities = variant.finals()
                points = 0
                for i in possibilities:
                    if i.check_winner() == 'x':
                        points += 1
                    elif i.check_winner() == 'o':
                        points -= 1
                return points
            else:
                return None
        if variant2:
            choice = max(variant1, variant2, key=find_points).key
            return self._board.difference(choice)
        else:
            return self._board.difference(variant1.key)





if __name__ == '__main__':
    g = Game()
    g.start_game()