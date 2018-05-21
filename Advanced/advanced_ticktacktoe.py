import anytree

from game import Game


class AdvancedGame(Game):

    def make_decision_tree(self):
        """
        (AdvancedGame) -> (anytree.Node)
        Makes a decision tree for given position
        """
        tree = anytree.Node(name='', board=self._board)

        def another(player):
            """
            (str) -> (str)
            Returns another player symbol
            """
            if player == 'x':
                return 'o'
            elif player == 'o':
                return 'x'

        def make_board(board, turn, player):
            """
            (Board, tuple, str) -> (board)
            Makes a board with  a given turn
            """
            result = board.copy()
            i, j = turn
            result[i, j] = player
            return result

        def fork_from_root(tree, current_player):
            """
            (anytree.Node, str) -> (anytree.Node)
            Recursive helper funtion
            """
            turns = tree.board.possible_turns()
            if turns:
                for i in range(len(turns)):
                    board = make_board(tree.board, turns[i], current_player)
                    board = anytree.Node(name='', board=board, parent=tree)
                    if not board.board.check_winner():
                        fork_from_root(board, another(current_player))

        fork_from_root(tree, 'x')
        return tree

    def choose_turn(self):
        """
        (AdvancedGame) -> (Board)
        Chooses a best turn
        """

        def finals(variant):
            ends = []
            if not variant.children:
                ends.append(variant)
            else:
                for i in variant.children:
                    ends += finals(i)
            return ends

        def find_points(variant):
            """
            (anytree.Node) -> (float/None)
            Calculates a rating of any position
            """
            if variant:
                possibilities = finals(variant)
                points = 0
                for i in possibilities:
                    if i.board.check_winner() == 'x':
                        points += 1
                    elif i.board.check_winner() == 'o':
                        points -= 1
                return points
            else:
                return None

        decision_tree = self.make_decision_tree()
        variants = list(decision_tree.children)
        variants = list(filter(lambda x: x, variants))
        choice = max(variants, key=find_points).board
        return self._board.difference(choice)


if __name__ == '__main__':
    g = AdvancedGame()
    g.start_game()
