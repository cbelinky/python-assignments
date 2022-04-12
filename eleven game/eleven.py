""" A text-based implementation of (parts of) the game 2048 by Gabriele
Cirulli. See https://play2048.co/ for more information on the original
game.

In the original, like numbers sum together to form increasing powers of
2. In this version, like numbers are incremented by 1 to form increasing
integers. You can think of these numbers as exponents of the number 2.
"""

from copy import deepcopy
import os
import platform
import random


# the probability of getting a 1 rather than a 2
PROB_1 = 0.9
# the possible directions
DIRECTIONS = ["up", "down", "left", "right"]


class DirectionError(Exception):
    """ A custom error to raise if the board will not allow movement in
    the requested direction. """
    pass


class Board:
    """A modified 2048 board. In 2048, the non-empty cells contain
    powers of 2. In this game, they contain numbers 1-11, which can be 
    thought of as exponents to which the number 2 could be raised.
    
    Attributes:
        width (int): an integer not less than 3.
        matrix (list of (int or None)): the board, represented as a one-
            dimensional list. Items 0 through self.width-1 represent the
            first row; items self.width to (2*self.width)-1 represent
            the second row; and so on.
        cache (dict of str: tuple of (list of (int or None)), int):
            results of previous calls to the calculate_move() method for
            the current state of the board. (Saves some time at the
            expense of some memory.)
    """
    
    def __init__(self, width=4):
        """ Create a board of the specified size containing two
        randomly-placed starting numbers.
        
        Args:
            width (int): an integer not less than 3 representing the
                width (and height) of the board.
        
        Side effects:
            Sets attributes width and matrix.
        
        Raises:
            ValueError: specified width is too small.
        """
        if width < 3:
            raise ValueError("width is too small")
        self.width = width
        self.matrix = [None] * (width ** 2)
        self.cache = {}
        for i in range(2):
            self.new_number()
            
    def is_winner(self):
        """ Returns True if the current state of the board reflects a
        win. """
        return 11 in self.matrix
    
    def free_spaces(self):
        """ Returns a list of indices in self.matrix where the value is
        None. (These are available spaces.) """
        return [i for i, space in enumerate(self.matrix) if space is None]
    
    def new_number(self):
        """ Insert a 1 or a 2 in a random position on the board. """
        pos = random.choice(self.free_spaces())
        num = 1 if random.random() < PROB_1 else 2
        self.matrix[pos] = num
        return pos, num

    def get_coord(self, pos):
        """ Convert pos to x, y coordinates.
        
        Args:
            pos (int): an index into self.matrix.
            
        Returns:
            tuple of int, int: the x and y coordinates that correspond
            to pos.
        
        Raises:
            ValueError: the specified position was out of range.
        """
        if not (0 <= pos < len(self.matrix)):
            raise ValueError("pos out of range")
        return pos % self.width, pos // self.width
    
    def get_pos(self, x, y):
        """ Convert x, y coordinates to an index into self.matrix.
        
        Args:
            x (int): an x coordinate.
            y (int): a y coordinate.
        
        Returns:
            int: the corresponding index into self.matrix.
        
        Raises:
            ValueError: at least one coordinate was out of range.
        """
        for coord, letter in [(x, "x"), (y, "y")]:
            if not (0 <= coord < self.width):
                raise ValueError("{} coordinate out of range".format(letter))
        return y * self.width + x
    
    def get_value(self, x, y):
        """ Get the current value of the cell at position x, y.
        
        Args:
            x (int): an x coordinate.
            y (int): a y coordinate.
        
        Returns:
            int or None: the current value of the cell at position x, y.
        
        Raises:
            ValueError: at least one coordinate was out of range.
        """
        for coord, letter in [(x, "x"), (y, "y")]:
            if not (0 <= coord < self.width):
                raise ValueError("{} coordinate out of range".format(letter))
        return self.matrix[self.get_pos(x, y)]
    
    def get_slice(self, coord, axis=0, matrix=None):
        """ Get one row or column of the board as a list.
        
        Args:
            coord (int): the x or y coordinate of the row or column.
            axis (int, optional): 0 to get a row; 1 to get a column.
                Defaults to 0.
            matrix (list of (int or None), optional): the matrix to be
                sliced. If None, use self.matrix. Defaults to None.
        
        Returns:
            list of (int or None): the contents of the requested row or
            column.
            
        Raises:
            ValueError: at least one coordinate is out of range.
            ValueError: an invalid value was given for the axis
                parameter.
        """
        if not (0 <= coord < self.width):
            raise ValueError("coordinate must be between 0 and {}"
                             .format(self.width - 1))
        if axis not in [0, 1]:
            raise ValueError("axis must be 0 (row) or 1 (column)")
        if matrix is None:
            matrix = self.matrix
        step1, step2 = (1, self.width) if axis == 0 else (self.width, 1)
        start = coord * step2
        end = (start + self.width) * step1
        return matrix[start:end:step1]
    
    def transpose(self, matrix):
        """ Return a version of matrix with the rows turned into
        columns and vice versa.
        
        Args:
            matrix (list of (int or None)): a board similar to
                self.matrix.
        
        Returns:
            list of (int or None): the transposed matrix.
            
        Raises:
            ValueError: matrix is not the same size as the current
                board.
        """
        if len(matrix) != self.width ** 2:
            print(matrix)
            print(len(matrix))
            raise ValueError("matrix must be the same size as the board")
        return [n for s in 
                [self.get_slice(i, axis=1, matrix=matrix)
                 for i in range(self.width)]
                for n in s]
    
    def is_valid_direction(self, direction):
        """ Determine whether direction is a known direction (up, down,
        etc.). """
        return direction in DIRECTIONS
    
    def calculate_move(self, direction):
        """ Without changing the board itself, determine how the current
        board would change and how many points the user would earn if
        the board were moved in a specific direction.
        
        Args:
            direction (str): should be "up", "down", "left", or "right".
            
        Returns:
            tuple of (list of (int or None)), int: the new state of the
                board if it were moved in the specified direction, and
                the points that would be earned in that case.
                
        Raises:
            ValueError: specified direction is not a recognized
                direction (e.g., "up", "down", "left", or "right").
            DirectionError: specified direction is not valid given the
                current state of the board.
                
        Side effects:
            May modify self.cache.
        """
        if direction in self.cache:
            if self.cache[direction] == DirectionError:
                raise DirectionError
            else:
                return self.cache[direction]
        if not self.is_valid_direction(direction):
            raise ValueError("invalid direction: {}".format(direction))
        axis = 1 if direction in ["up", "down"] else 0
        reverse = direction in ["down", "right"]
        new_matrix = []
        points = 0
        for i in range(self.width):
            values = [v for v in self.get_slice(i, axis=axis) if v]
            if reverse:
                values.reverse()
            new_values = []
            while values:
                v1 = values.pop(0)
                if v1 is None:
                    continue
                if values and values[0] == v1:
                    values.pop(0)
                    new_values.append(v1+1)
                    points += (v1 + 1) ** 2
                else:
                    new_values.append(v1)
            if len(new_values) < self.width:
                new_values += [None] * (self.width - len(new_values))
            if reverse:
                new_values.reverse()
            new_matrix.extend(new_values)
        if axis == 1:
            new_matrix = self.transpose(new_matrix)
        if new_matrix == self.matrix:
            self.cache[direction] = DirectionError
            raise DirectionError
        self.cache[direction] = new_matrix, points
        return new_matrix, points
    
    def move(self, direction):
        """ Move the contents of the board in the specified direction.
        
        Args:
            direction (str): should be "up", "down", "left", or "right".
        
        Returns:
            int: the number of points earned for this move.
        
        Side effects:
            Alters self.matrix and self.cache.
        
        Raises:
            ValueError: specified direction is not valid given the
                current state of the board.
        """
        if not self.is_valid_direction(direction):
            raise ValueError("invalid direction: {}".format(direction))
        try:
            matrix, points = self.calculate_move(direction)
        except DirectionError:
            raise
        self.cache.clear()
        self.matrix = matrix
        return points
    
    def is_valid_move(self, direction):
        """ Determines whether the specified direction is a valid move
        given the current state of the board. A move is valid if at
        least one number on the board would be different or would move
        to a different location as a result of the move. """
        if not self.is_valid_direction(direction):
            raise ValueError("invalid direction: {}".format(direction))
        try:
            self.calculate_move(direction)
        except DirectionError:
            return False
        return True

    def valid_moves(self):
        """ Return a list of all possible moves given the current state
        of the board. """
        return [d for d in DIRECTIONS if self.is_valid_move(d)]
    

    def __str__(self):
        """ Convert the board to a string representation suitable for
        printing to the console. """
        rows = []
        max_val = max(n or 0 for n in self.matrix)
        min_width = max(len(str(max_val)), 2)
        cell_template = "{:>MWs}".replace("MW", str(min_width))
        row_template = "|" + "|".join([cell_template]*self.width) + "|"
        line = "+" + (("-"*min_width)+"+") * self.width
        rows.append(line)
        for i in range(self.width):
            values = ["" if n is None else str(n) for n in self.get_slice(i)]
            rows.append(row_template.format(*values))
            rows.append(line)
        return "\n".join(rows)
    
    def __copy__(self):
        """ Create a shallow copy of a Board object. It's safer to use
        __deepcopy__() instead of __copy__()."""
        new_board = Board(width=self.width)
        new_board.matrix = self.matrix
        new_board.cache = self.cache
        return new_board
    
    def __deepcopy__(self, memo=None):
        """ Create a deep copy of a Board object. """
        if memo is None:
            memo = {}
        new_board = Board(width=self.width)
        new_board.matrix = deepcopy(self.matrix, memo=memo)
        new_board.cache = deepcopy(self.cache, memo=memo)
        return new_board
        
    def __eq__(self, other):
        """ Define the behavior of the == operator for Board objects. """
        return self.matrix == other.matrix
    
    def __ne__(self, other):
        """ Define the behavior of the != operator for Board objects. """
        return not self.__eq__(other)


class Player:
    """ Abstract class for players of the game. Each subclass of this
    class should, at a minimum, implement the get_move() method.
    
    The Player method (or a subclass of it) is responsible for "running"
    the game. This happens in the play() method.
    
    Attributes:
        board (Board): the game board.
        score (int): the player's score.
    """
    def __init__(self):
        """ Create a new player object. """
        self.board = Board()
        self.score = 0
    
    def play(self):
        """ Play a game of 2048. As long as the game has not been won or
        lost, Call self.get_move() to find out the player's move. Then
        update the board and score accordingly. """
        while self.board.valid_moves() and not self.board.is_winner():
            direction = self.get_move()
            self.score += self.board.move(direction)
            if self.board.is_winner():
                return True
            self.board.new_number()
        return False
        
    def get_move(self):
        """ Indicate a direction in which to move the contents of the
        board. It is the responsibility of the Player subclass to
        ensure that the specified direction is allowable (the
        valid_moves() method of self.board will give you the list of
        possible values).
        
        DO NOT call the move() method of self.board in this method.
        Instead, return the direction in which to move.
        
        Returns:
            str: the direction in which to move (should be "up", "down",
            "left", or "right").
        """
        raise NotImplementedError


def clear_screen():
    """ Convenience function that you can use to clear the terminal
    screen after each move. """
    cmd = "cls" if platform.system() == "Windows" else "clear"
    os.system(cmd)


def test_player(cls, iterations=100):
    """ Have a computer player play several games and return the average
    score of these games, in order to evaluate the strength of the
    player's decision-making abilities.
    
    Args:
        cls (Player): a subclass of the Player class.
        iterations (int): the number of trials to do.
    
    Returns:
        float: the average score over the trials performed.
    """
    assert issubclass(cls, Player), "cls must be a subclass of Player"
    total = 0
    for i in range(iterations):
        p = cls()
        p.play()
        total += p.score
    return total / iterations
