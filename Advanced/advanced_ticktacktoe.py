from game import Game
import anytree


class AdvancedGame(Game):

    def make_decision_tree(self):
        tree  = anytree.Node(name='', board=self._board)

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

        def fork_from_root(tree, current_player):
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
        def finals(variant):
            ends = []
            if not variant.children:
                ends.append(variant)
            else:
                for i in variant.children:
                    ends += finals(i)
            return ends

        def find_points(variant):
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

