# Author: Zhangfan Li
import random
import copy


class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    # Helper methods to check if is in drop phase
    def check_drop(self, state):
        count = 0
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 'r' or state[i][j] == 'b':
                    count = count + 1
        if (count >= 8):
            return False
        else:
            return True

    # Return a list of successors based on current state
    def succ(self, state, marker):
        succ = []
        drop_phase = self.check_drop(state)

        if drop_phase:
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j] == ' ':
                        temp = copy.deepcopy(state)
                        temp[i][j] = marker
                        succ.append(temp)
        else:
            for i in range(len(state)):
                for j in range(len(state[i])):
                    # move markers
                    if state[i][j] == marker:
                        # down
                        temp = copy.deepcopy(state)
                        if i + 1 < len(temp) and temp[i + 1][j] == ' ':
                            temp[i][j] = ' '
                            temp[i + 1][j] = marker
                            succ.append(temp)
                        # up
                        temp = copy.deepcopy(state)
                        if i - 1 >= 0 and temp[i - 1][j] == ' ':
                            temp[i][j] = ' '
                            temp[i - 1][j] = marker
                            succ.append(temp)
                        # right
                        temp = copy.deepcopy(state)
                        if j + 1 < len(temp) and temp[i][j + 1] == ' ':
                            temp[i][j] = ' '
                            temp[i][j + 1] = marker
                            succ.append(temp)
                        # left
                        temp = copy.deepcopy(state)
                        if j - 1 >= 0 and temp[i][j - 1] == ' ':
                            temp[i][j] = ' '
                            temp[i][j - 1] = marker
                            succ.append(temp)
                        # downleft
                        temp = copy.deepcopy(state)
                        if i + 1 < len(temp) and j - 1 >= 0 and temp[i + 1][j - 1] == ' ':
                            temp[i][j] = ' '
                            temp[i + 1][j - 1] = marker
                            succ.append(temp)
                        # downright
                        temp = copy.deepcopy(state)
                        if i + 1 < len(temp) and j + 1 < len(temp) and temp[i + 1][j + 1] == ' ':
                            temp[i][j] = ' '
                            temp[i + 1][j + 1] = marker
                            succ.append(temp)
                        # upleft
                        temp = copy.deepcopy(state)
                        if i - 1 >= 0 and j - 1 >= 0 and temp[i - 1][j - 1] == ' ':
                            temp[i][j] = ' '
                            temp[i - 1][j - 1] = marker
                            succ.append(temp)
                        # upright
                        temp = copy.deepcopy(state)
                        if i - 1 >= 0 and j + 1 < len(temp) and temp[i - 1][j + 1] == ' ':
                            temp[i][j] = ' '
                            temp[i - 1][j + 1] = marker
                            succ.append(temp)

        return succ

    # Helper method to calculate heuristic value for horizontal
    def cal_hor(self, state, marker):
        max = 0
        count = 0
        for i in range(len(state)):
            jump = False
            for j in range(len(state) - 1):
                if state[i][j] == marker:
                    count = count + 1
                    n = 0
                    while state[i][j] == state[i][j + 1]:
                        count = count + 1
                        j = j + 1
                        n = n + 1
                        if n >= 3:
                            return count / 4
                        if j >= len(state) - 1:
                            jump = True
                            break

                if max < count:
                    max = count
                count = 0
                if jump:
                    break
        return max / 4

    # Helper method to calculate heuristic value for vertical
    def cal_ver(self, state, marker):
        max = 0
        count = 0
        for i in range(len(state)):
            jump = False
            for j in range(len(state) - 1):
                if state[j][i] == marker:
                    count = count + 1
                    n = 0
                    while state[j][i] == state[j + 1][i]:
                        count = count + 1
                        j = j + 1
                        n = n + 1
                        if n >= 3:
                            return count / 4
                        if j >= len(state) - 1:
                            jump = True
                            break
                if max < count:
                    max = count
                count = 0
                if jump:
                    break
        return max / 4

    # Helper method to calculate heuristic value for diagonal /
    def cal_dia_right(self, state, marker):
        max = 0
        count = 0
        for i in range(len(state) - 1):
            jump = False
            for j in range(len(state) - 1):
                if state[i][j] == marker:
                    count = count + 1
                    n = 0
                    while state[i][j] == state[i + 1][j + 1]:
                        count = count + 1
                        i = i + 1
                        j = j + 1
                        n = n + 1
                        if n >= 3:
                            return count / 4
                        if j >= len(state) - 1 or i >= len(state) - 1:
                            jump = True
                            break
                if max < count:
                    max = count
                count = 0
                if jump:
                    break
        return max / 4

    # Helper method to calculate heuristic value for diagonal \
    def cal_dia_left(self, state, marker):
        max = 0
        count = 0
        for i in range(2, len(state)):
            jump = False
            for j in range(len(state) - 1):
                if state[i][j] == marker:
                    count = count + 1
                    n = 0
                    while state[i][j] == state[i - 1][j + 1]:
                        count = count + 1
                        i = i - 1
                        j = j + 1
                        n = n + 1
                        if n >= 3:
                            return count / 4
                        if i < 0 or j >= len(state) - 1:
                            jump = True
                            break
                if max < count:
                    max = count
                count = 0
                if jump:
                    break
        return max / 4

    # Helper method to calculate heuristic value for diamond
    def cal_diamond(self, state, marker):
        max = 0
        count = 0
        for i in range(len(state) - 2):
            for j in range(1, len(state) - 1):
                if state[i][j] == marker and state[i + 1][j] == ' ':
                    count = count + 1
                if state[i + 1][j + 1] == marker:
                    count = count + 1
                if state[i + 2][j] == marker:
                    count = count + 1
                if state[i + 1][j - 1] == marker:
                    count = count + 1
                if max < count:
                    max = count
                count = 0
        return max / 4

    # Calculate heuristic value for current state
    def heuristic_game_value(self, state):
        # check if is terminal state
        terminal = self.game_value(state)
        if terminal == 1 or terminal == -1:
            return terminal, state

        my = []
        opp = []

        # heuristic of my
        my.append(self.cal_hor(state, self.my_piece))
        my.append(self.cal_ver(state, self.my_piece))
        my.append(self.cal_dia_left(state, self.my_piece))
        my.append(self.cal_dia_right(state, self.my_piece))
        my.append(self.cal_diamond(state, self.my_piece))

        # heuristic of opp
        opp.append(self.cal_hor(state, self.opp))
        opp.append(self.cal_ver(state, self.opp))
        opp.append(self.cal_dia_left(state, self.opp))
        opp.append(self.cal_dia_right(state, self.opp))
        opp.append(self.cal_diamond(state, self.opp))

        max_score = max(my)
        min_score = max(opp)

        return max_score + (-1) * min_score, state

    # Find the max heuristic value in the given depth, which is 2 here
    # Return if it is a terminal state
    def Max_Value(self, state, depth):
        max_state = copy.deepcopy(state)
        if self.game_value(state) != 0:
            return self.game_value(state), state

        if depth > 2:
            return self.heuristic_game_value(state)

        else:
            a = float('-Inf')
            for s in self.succ(state, self.my_piece):
                if self.game_value(s) != 0:
                    return self.game_value(s), s
                val, curr = self.Min_Value(s, depth + 1)
                if val > a:
                    a = val
                    max_state = s
        return a, max_state

    # Find the min heuristic value in the given depth, which is 2 here
    # Return if it is a terminal state
    def Min_Value(self, state, depth):
        min_state = copy.deepcopy(state)
        if self.game_value(state) != 0:
            return self.game_value(state), state

        if depth > 2:
            return self.heuristic_game_value(state)

        else:
            b = float('Inf')
            for s in self.succ(state, self.opp):
                if self.game_value(s) != 0:
                    return self.game_value(s), s
                val, curr = self.Max_Value(s, depth + 1)
                if val < b:
                    b = val
                    min_state = s
        return b, min_state

    # Helper methods to find different position in two states
    def state_diff(self, state, next):
        pos = []
        for i in range(5):
            for j in range(5):
                if state[i][j] != next[i][j]:
                    dif = [i, j]
                    pos.append(dif)
        return pos

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        drop_phase = self.check_drop(state)  # detect drop phase

        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            move = []
            a, next = self.Max_Value(state, 0)
            pos = self.state_diff(state, next)
            # find previous pos
            if state[pos[0][0]][pos[0][1]] == ' ':
                (pre_row, pre_col) = (pos[1][0], pos[1][1])
                (row, col) = (pos[0][0], pos[0][1])
            else:
                (pre_row, pre_col) = (pos[0][0], pos[0][1])
                (row, col) = (pos[1][0], pos[1][1])
            move.insert(0, (row, col))
            move.insert(1, (pre_row, pre_col))
            return move

        # TODO: implement a minimax algorithm to play better
        move = []
        a, next = self.Max_Value(state, 0)
        pos = self.state_diff(state, next)
        (row, col) = (pos[0][0], pos[0][1])
        while not state[row][col] == ' ':
            (row, col) = (pos[0][0], pos[0][1])

        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, (row, col))
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][
                        col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # check \ diagonal wins
        for row in range(2):
            for i in range(2):
                if state[row][i] != ' ' and state[row][i] == state[row + 1][i + 1] == state[row + 2][i + 2] == \
                        state[row + 3][i + 3]:
                    return 1 if state[row][i] == self.my_piece else -1

        # check / diagonal wins
        for row in range(3, 5):
            for i in range(2):
                if state[row][i] != ' ' and state[row][i] == state[row - 1][i + 1] == state[row - 2][i + 2] == \
                        state[row - 3][i + 3]:
                    return 1 if state[row][i] == self.my_piece else -1

        # check diamond wins
        for row in range(1, 4):
            for i in range(3):
                if state[row][i] != ' ' and state[row][i] == state[row - 1][i + 1] == state[row][i + 2] == \
                        state[row + 1][i + 1] and state[row][i + 1] == ' ':
                    return 1 if state[row][i] == self.my_piece else -1

        return 0  # no winner yet


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                      (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
