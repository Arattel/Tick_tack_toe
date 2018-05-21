import random

from arrays import Array2D


class Board(Array2D):
    def __init__(self):
        super().__init__(3, 3)

    def __str__(self):
        s = ' git  0 1 2\n'
        for i in range(3):
            s += '{}|'.format(i)
            for j in range(3):
                if self[i, j]:
                    s += self[i, j] + '|'
                else:
                    s += ' |'
            s += '\n'
        return s

    def _check_diag1(self):
        first = self[0, 0]
        if first is None:
            return False
        for i in range(1, 3):
            if self[i, i] != first:
                return False
        return first

    def _check_diag2(self):
        first = self[0, 2]
        if first is None:
            return False
        for i in range(3):
            j = 2 - i
            if self[i, j] != first:
                return False
        return first

    def _check_horiz(self):
        for i in range(3):
            first = self[i, 0]
            row = first is not None
            if row:
                for j in range(3):
                    if self[i, j] != first:
                        row = False
            if row:
                return first
        return False

    def _check_vert(self):
        for i in range(3):
            first = self[0, i]
            col = first is not None
            if col:
                for j in range(3):
                    if self[j, i] != first:
                        col = False
            if col:
                return first
        return False

    def check_winner(self):
        for i in [self._check_diag1(), self._check_diag2(), self._check_horiz(), self._check_vert()]:
            if i:
                return i
        return False

    def possible_turns(self):
        turns = []
        for i in range(3):
            for j in range(3):
                if not self[i, j]:
                    turns.append((i, j))
        return turns

    def random_possible_turns(self):
        possible_turns = self.possible_turns()
        if len(possible_turns) > 1:
            left = random.choice(possible_turns)
            right = random.choice(possible_turns)
            while left == right:
                right = random.choice(possible_turns)
            return left, right
        elif len(possible_turns) > 0:
            return possible_turns[0], None
        else:
            return None, None

    def copy(self):
        copy_board = Board()
        for i in range(3):
            for j in range(3):
                copy_board[i, j] = self[i, j]
        return copy_board

    def difference(self, another):
        for i in range(3):
            for j in range(3):
                if self[i, j] != another[i, j]:
                    return i, j

    def is_filled(self):
        for i in range(3):
            for j in range(3):
                if self[i, j] is None:
                    return False
        return True


if __name__ == '__main__':
    a = Board()
    a[0, 0] = 'o'
    a[1, 1] = 'o'
    a[2, 2] = 'o'
    b = a.copy()
    b[0, 1] = 'x'
    print(a)
    print(b)
    print(a.check_winnner())
