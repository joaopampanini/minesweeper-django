import random

from django.db import models


class Game(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    won = models.BooleanField(default=False)
    cells = models.PositiveIntegerField(default=0)
    opened = models.PositiveIntegerField(default=0)
    board = models.JSONField()
    mines = models.JSONField()

    def create_board(self, m_x, m_y, num_mines):
        board = [[0]*m_x]*m_y
        mines = []

        while len(mines) < num_mines:
            x = random.randint(0, m_x - 1)
            y = random.randint(0, m_y - 1)

            if board[y][x] >= 0:
                board[y][x] = -1  # mine value
                mines.append([x, y])

                if x != m_x - 1 and board[y][x + 1] != -1:
                    board[y][x + 1] = board[y][x + 1] + 1

                if x != 0 and board[y][x - 1] != -1:
                    board[y][x - 1] = board[y][x - 1] + 1

                if y != m_y - 1 and board[y + 1][x] != -1:
                    board[y + 1][x] = board[y + 1][x] + 1

                if y != 0 and board[y - 1][x] != -1:
                    board[y - 1][x] = board[y - 1][x] + 1

                if y != m_y - 1 and x != m_x - 1 and board[y + 1][x + 1] != -1:
                    board[y + 1][x + 1] = board[y + 1][x + 1] + 1

                if y != m_y - 1 and x != 0 and board[y + 1][x - 1] != -1:
                    board[y + 1][x - 1] = board[y + 1][x - 1] + 1

                if y != 0 and x != m_x - 1 and board[y - 1][x + 1] != -1:
                    board[y - 1][x + 1] = board[y - 1][x + 1] + 1

                if y != 0 and x != 0 and board[y - 1][x - 1] != -1:
                    board[y - 1][x - 1] = board[y - 1][x - 1] + 1

        self.board = board
        self.mines = mines
        self.cells = m_x * m_y
        self.save()

    def open_cell(self, x, y, opened=[]):
        pass

    def open_neighbors(self, x, y, opened):
        pass
