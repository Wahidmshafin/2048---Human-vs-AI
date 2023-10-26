import random
import numpy as np
import math

height = 4
width = 4


class AI:
    def stack(board):
        global height, width
        new_matrix = [[0] * width for _ in range(height)]

        for i in range(height):
            fill_position = 0
            for j in range(width):
                if board[i][j] != 0:
                    new_matrix[i][fill_position] = board[i][j]
                    fill_position += 1
        return new_matrix

    def combine(board):
        score = 0
        for i in range(height):
            for j in range(width - 1):
                if board[i][j] != 0 and board[i][j] == board[i][j + 1]:
                    board[i][j] *= 2
                    board[i][j + 1] = 0
                    score += board[i][j] * 10
        return score, board

    def reverse(board):
        global height, width
        new_matrix = []
        for i in range(height):
            new_matrix.append([])
            for j in range(width):
                new_matrix[i].append(board[i][width - 1 - j])
        return new_matrix

    def transpose(board):
        global height, width
        new_matrix = [[0] * width for _ in range(height)]
        for i in range(height):
            for j in range(width):
                new_matrix[i][j] = board[j][i]
        return new_matrix

    def left(board):
        board = AI.stack(board)
        score, board = AI.combine(board)
        board = AI.stack(board)
        board = AI.new_tile(board)
        return score, board

    def right(board):
        board = AI.reverse(board)
        board = AI.stack(board)
        score, board = AI.combine(board)
        board = AI.stack(board)
        board = AI.reverse(board)
        board = AI.new_tile(board)
        return score, board

    def up(board):
        board = AI.transpose(board)
        board = AI.stack(board)
        score, board = AI.combine(board)
        board = AI.stack(board)
        board = AI.transpose(board)
        board = AI.new_tile(board)
        return score, board

    def down(board):
        board = AI.transpose(board)
        board = AI.reverse(board)
        board = AI.stack(board)
        score, board = AI.combine(board)
        board = AI.stack(board)
        board = AI.reverse(board)
        board = AI.transpose(board)
        board = AI.new_tile(board)
        return score, board

    def new_tile(board):
        global height, width
        for i in range(height):
            for j in range(width):
                if board[i][j] == 0:
                    board[i][j] = 2
                    return board
        return board

    def minmax(board, depth, alpha, beta, maximize):
        if depth == 10:
            return 0
        if maximize:
            beta = np.Infinity
            maxval = 0
            l_score, tmpboard = AI.left(board)
            l_score = l_score + AI.minmax(
                tmpboard, depth + 1, alpha, beta, not maximize
            )
            # maxval = max(l_score, maxval)
            maxval = l_score
            alpha = max(alpha, l_score)
            if beta <= alpha:
                return maxval
            r_score, tmpboard = AI.right(board)
            r_score = r_score + AI.minmax(
                tmpboard, depth + 1, alpha, beta, not maximize
            )
            maxval = max(r_score, maxval)
            alpha = max(alpha, r_score)
            if beta <= alpha:
                return maxval

            u_score, tmpboard = AI.up(board)
            u_score = u_score + AI.minmax(
                tmpboard, depth + 1, alpha, beta, not maximize
            )
            maxval = max(u_score, maxval)
            alpha = max(alpha, u_score)
            if beta <= alpha:
                return maxval
            d_score, tmpboard = AI.down(board)
            d_score = d_score + AI.minmax(
                tmpboard, depth + 1, alpha, beta, not maximize
            )
            alpha = max(alpha, d_score)
            maxval = max(d_score, maxval)
            return maxval

        else:
            beta = np.Infinity
            minval = np.Infinity
            l_score, tmpboard = AI.left(board)
            l_score = l_score + AI.minmax(
                tmpboard, depth + 1, alpha, beta, not maximize
            )
            minval = min(minval, l_score)
            # beta = min(beta, l_score)
            beta = l_score
            if beta <= alpha:
                return minval
            r_score, tmpboard = AI.right(board)
            r_score = r_score + AI.minmax(
                tmpboard, depth + 1, alpha, beta, not maximize
            )
            minval = min(minval, r_score)
            beta = min(beta, r_score)
            if beta <= alpha:
                return minval
            u_score, tmpboard = AI.up(board)
            u_score = u_score + AI.minmax(
                tmpboard, depth + 1, alpha, beta, not maximize
            )
            minval = min(minval, u_score)
            beta = min(beta, u_score)
            if beta <= alpha:
                return minval
            d_score, tmpboard = AI.down(board)
            d_score = d_score + AI.minmax(
                tmpboard, depth + 1, alpha, beta, not maximize
            )
            minval = min(minval, d_score)
            beta = min(beta, d_score)
            return minval

    def main(board):
        # global board
        # board = np.zeros((4, 4), dtype=np.int64)
        alpha = 0
        beta = np.Infinity
        score = 0
        l_score, tmpboard = AI.left(board)
        l_score = l_score + AI.minmax(tmpboard, 1, alpha, beta, False)
        score = l_score
        move = "left"

        r_score, tmpboard = AI.right(board)
        r_score = r_score + AI.minmax(tmpboard, 1, alpha, beta, False)
        if score < r_score:
            score = r_score
            move = "right"

        u_score, tmpboard = AI.up(board)
        u_score = u_score + AI.minmax(tmpboard, 1, alpha, beta, False)
        if score < u_score:
            score = u_score
            move = "up"

        d_score, tmpboard = AI.down(board)
        d_score = d_score + AI.minmax(tmpboard, 1, alpha, beta, False)
        if score < d_score:
            score = d_score
            move = "down"

        return move

    def check_draw(board):
        global height, width
        point = 0
        lboard = np.copy(board)
        a, lboard = AI.left(lboard)
        point = point + a
        rboard = np.copy(board)
        a, rboard = AI.right(rboard)
        point = point + a
        uboard = np.copy(board)
        a, uboard = AI.up(uboard)
        point = point + a
        dboard = np.copy(board)
        a, dboard = AI.down(dboard)
        point = point + a
        zero = False
        for i in range(height):
            for j in range(width):
                if board[i][j] == 0:
                    zero = True
        if lboard == rboard == dboard == uboard and point == 0 and not zero:
            return True

        return False
