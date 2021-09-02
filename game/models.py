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
        """Create board mines and neighbors mine counter for cells."""
        board = [[0]*m_x for i in range(m_y)]  # Initialize board with '0's
        mines = []

        # Iterate until all mines are created
        while len(mines) < num_mines:
            # Get a random x and y within game board
            x = random.randint(0, m_x - 1)
            y = random.randint(0, m_y - 1)

            # If (x,y)  value is -1, it is already a mine, so discard
            # and get a new one until a valid (x,y) is taken
            if board[y][x] >= 0:
                board[y][x] = -1  # Mine value
                mines.append([x, y])  # Add mine coordinates to mine list

                # The objective here is to incremente mine's neighbors value
                # indicating that that neighbor has a mine near them, each
                # cell start with zero and each mine add 1 to each neighbor
                # that is not a mine (value -1). It is easier to create
                # how many mines there is around a cell like this, the downside
                # is that use more space than just keeping the mines
                # coordinates
                #
                # All 'IF' clauses bellow are to check board limites, x and y
                # can't always access all 8 neighbors araound then, eg.: (0,0)
                # has just (1, 0), (0, 1) and (1, 1) as valid neighbors
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
        self.cells = m_x * m_y  # Value used to check if game has ended
        self.save()

    def get_game_state(self):
        """Check game state.

        If number of cells subtracted of the number of opened cells is equal
        the number of mines, it means that there is just mine cells unopened on
        game's board and the player won the game.
        """
        if len(self.mines) == self.cells - self.opened:
            self.end_date = timezone.now()
            self.save()

            return 'won'

        else:
            return 'continue'

    def click_handler(self, x, y):
        """Handle prlayer's click."""

        # Check if it is the first click and add start date
        if self.opened == 0:
            self.start_date = timezone.now()
            self.save()

        # Off board coordinates, force a game-over
        if x >= len(self.board[0]) or y >= len(self.board) or x < 0 or y < 0:
            return {
                'result': 'game-over',
                'mines': self.mines
            }

        # Check if coordinates are from a mine cell and trigger game-voer
        if self.board[y][x] == -1:
            self.end_date = timezone.now()
            self.save()

            return {
                'result': 'game-over',
                'mines': self.mines
            }

        else:
            # If not a mine, open clicked cell
            opened = self.open_cell(x, y, [])

            return {
                'result': self.get_game_state(),
                'opened': opened
            }

    def open_cell(self, x, y, opened):
        """Open (x,y) cell."""

        # check if coordinates are not opened (Null value) or is not a mine
        if self.board[y][x] is not None and self.board[y][x] != -1:
            # If not, open cell applying Null value to it.
            value = self.board[y][x]

            # Add cell's coordinates and value to be returned and visible on
            # front-end
            opened.append([x, y, value])
            self.board[y][x] = None  # Opened value
            self.opened = self.opened + 1  # Incremente opened count
            self.save()

            # If cell's value is zero, try to open all it's neighbors
            if value == 0:
                opened = self.open_neighbors(x, y, opened)

        return opened

    def open_neighbors(self, x, y, opened):
        """Open all (x,y)'s neighbors."""
        m_x = len(self.board[0])  # Get x limite
        m_y = len(self.board)  # Get y limite

        # All 'IF' clauses bellow are to check board limites, x and y
        # can't always access all 8 neighbors araound then, eg.: (0,0)
        # has just (1, 0), (0, 1) and (1, 1) as valid neighbors
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
