import random

from django.db import models
from django.utils import timezone


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
        board = [[0]*m_x for i in range(m_y)]
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

    def get_game_state(self):
        if len(self.mines) == self.cells - self.opened:
            self.end_date = timezone.now()
            self.save()

            return 'won'

        else:
            return 'continue'

    def click_handler(self, x, y):
        if self.opened == 0:
            self.start_date = timezone.now()
            self.save()

        if x < 0 or y < 0:
            return {
                'result': 'game-over',
                'mines': self.mines
            }

        if x >= len(self.board[y][x]) or y >= len(self.board[y]):
            return {
                'result': 'game-over',
                'mines': self.mines
            }

        if self.board[y][x] == -1:
            self.end_date = timezone.now()
            self.save()

            return {
                'result': 'game-over',
                'mines': self.mines
            }

        else:
            opened = self.open_cell(x, y, [])

            return {
                'result': self.get_game_state(),
                'opened': opened
            }

    def open_cell(self, x, y, opened):
        if self.board[y][x] is not None and self.board[y][x] != -1:
            value = self.board[y][x]

            opened.append([x, y, value])
            self.board[y][x] = None
            self.opened = self.opened + 1
            self.save()

            if value == 0:
                opened = self.open_neighbors(x, y, opened)

        return opened

    def open_neighbors(self, x, y, opened):
        m_x = len(self.board[0])
        m_y = len(self.board)

        if x != m_x - 1:
            opened = self.open_cell(x + 1, y, opened)

        if x != 0:
            opened = self.open_cell(x - 1, y, opened)

        if y != m_y - 1:
            opened = self.open_cell(x, y + 1, opened)

        if y != 0:
            opened = self.open_cell(x, y - 1, opened)

        if y != m_y - 1 and x != m_x - 1:
            opened = self.open_cell(x + 1, y + 1, opened)

        if y != m_y - 1 and x != 0:
            opened = self.open_cell(x - 1, y + 1, opened)

        if y != 0 and x != m_x - 1:
            opened = self.open_cell(x + 1, y - 1, opened)

        if y != 0 and x != 0:
            opened = self.open_cell(x - 1, y - 1, opened)

        return opened
