from eleven import Player
from eleven import Board
import random

class HumanPlayer(Player):
    def __init__(self):
        """ Create a new player object. Inherited from Player class.
        """
        super().__init__()
    
    def get_move(self): 
        """ Takes user input to indicate a direction in which to move the 
        contents of the board.
        
        Returns:
            str: the direction in which to move (should be "up", "down",
            "left", or "right").
        """
        print(self.score)
        print(self.board.__str__())
        while True:
            x = input("Enter a direction... ('up', 'down', 'left', 'right')")
            if x not in self.board.valid_moves():
                print("Please enter a valid move")
                continue
            else:
                return x
    
    def play(self):
        """ Play a game of 2048. As long as the game has not been won or
        lost, Call self.get_move() to find out the player's move. Then
        update the board and score accordingly. """
        result = Player.play(self)
        if result == True:
            print("You win!")
        else:
            print("Game over.")

class ComputerPlayer(Player):
    def __init__(self):
        """ Create a new player object. Inherited from Player class.
        """
        super().__init__()
    
    def get_move(self):
        """ randomly a direction in which to move the contents of the
        board.
        
        Returns:
            str: the direction in which to move (should be "up", "down",
            "left", or "right").
        """
        possible_moves = ['up', 'down', 'left', 'right']
        while True:
            x = random.choice(possible_moves)
            if x not in self.board.valid_moves():
                continue
            else:
                return x   

class ComputerPlayer2(ComputerPlayer):
    def __init__(self):
        """ Create a new player object. Inherited from Player class.
        """
        super().__init__()
    
    def play(self):
        """ Play a game of 2048. As long as the game has not been won or
        lost, Call self.get_move() to find out the player's move. Then
        update the board and score accordingly. """
        super().play()
    
    def get_move(self):
        """ uses heuristics to indicate a direction in which to move the 
        contents of the board.
        
        Returns:
            str: the direction in which to move (should be "up", "down",
            "left", or "right").
        """
        #heuristics: prioritizes empty spaces on the board. Completes a move 
        #depending on the number of empty spaces each move creates. 
        #More empty spaces on the board means more tiles are combined, which is
        #the main objective of the game and leads to a higher score.
        x = self.board #store board object in a variable
        #simulate each possible move, and store the number of empty spaces on 
        #the board as a result of the move.
        if 'up' in x.valid_moves():
            up = self.board.__copy__()
            up.move('up')
            len_up = len(up.free_spaces())
        else:
            len_up = 0
        if 'down' in x.valid_moves():
            down = self.board.__copy__()
            down.move('down')
            len_down = len(down.free_spaces())
        else:
            len_down = 0
        if 'left' in x.valid_moves():
            left = self.board.__copy__()
            left.move('left')
            len_left = len(left.free_spaces())
        else:
            len_left = 0
        if 'right' in x.valid_moves():
            right = self.board.__copy__()
            right.move('right')
            len_right = len(right.free_spaces())
        else:
            len_right = 0
        #compare the number of empty spaces each move leaves on the board 
        lengths = {len_up:"up", len_down:"down", len_left:"left", 
                   len_right:"right"}
        #find the move that leaves the most empty spaces on the board and 
        #returns it
        max_empty_spaces = lengths.get(max(lengths))
        return max_empty_spaces