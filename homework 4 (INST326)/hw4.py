import sys
class Maze:

    def __init__(self, path):
        self.load(path)

    def load(self, path):
        """
        Opens specified file for reading and converts the contents of the file into a list of strings and stores these in the object's maze attribute.

        Arguments:
            path -- str -- A path to a plain text file in UTF-8 encoding containing a maze.
        """
        f = open(path, 'r', encoding='utf-8')
        self.maze = []
        for line in f.readlines():
            line = line.rstrip('\n')
            self.maze.append(line)
        self.start = self.find_opening(0)
        self.end = self.find_opening(-1)

    def find_opening(self, pos):
        """Iterates over the strings in the object's maze attribute until it finds a string where the character at the specified position (0 or -1) is a space character.

        Arguments:
            pos -- int -- The position to at which to look for an opening. Should be 0 (start of the string) or -1 (end of the string).

        Returns:
            [tuple (int, int)] -- [returns start/end coordinates of object's maze attribute.]
        """
        if pos == 0:
            for y, x in enumerate(self.maze):
                if x[0] == ' ':
                    start = (0, y)
                    return start
        elif pos == -1:
            for y, x in enumerate(self.maze):
                if x[-1] == ' ':
                    end = ((len(x)-1), y)
                    return end

    def solve(self):
        """Finds a path of (x, y) coordinates through the maze specified in the
        object's maze attribute, where each x coordinate represents an index in
        a string and each y coordinate represents an index
        in the list of strings.

        Returns:
            list -- Returns a list of tuples that act as the coordinates of
            the fastest path needed to reach the end of the maze.
        """
        start = self.start
        end = self.end
        visited = [start]
        exploring = [visited.copy()]
        while 1 == 1:
            current_path = exploring.pop()
            current_cord = current_path[-1]
            if current_cord == end:
                return current_path
            (w, z) = current_cord
            if 0 <= w < end[0] and self.maze[z][w+1] == " " and (w+1, z) not in visited and (w+1, z) not in current_path:
                new_cord = (w+1, z)
                visited.append(new_cord)
                new_path = current_path.copy()
                new_path.append(new_cord)
                exploring.append(new_path)
            if 0 <= w < end[0] and self.maze[z][w-1] == " " and (w-1, z) not in visited and (w-1, z) not in current_path:
                new_cord = (w-1, z)
                visited.append(new_cord)
                new_path = current_path.copy()
                new_path.append(new_cord)
                exploring.append(new_path)
            if 0 <= w < end[0] and self.maze[z+1][w] == " " and (w, z+1) not in visited and (w, z+1) not in current_path:
                new_cord = (w, z+1)
                visited.append(new_cord)
                new_path = current_path.copy()
                new_path.append(new_cord)
                exploring.append(new_path)
            if 0 <= w < end[0] and self.maze[z-1][w] == " " and (w, z-1) not in visited and (w, z-1) not in current_path:
                new_cord = (w, z-1)
                visited.append(new_cord)
                new_path = current_path.copy()
                new_path.append(new_cord)
                exploring.append(new_path)

def main(path):
    my_maze = Maze(path)
    Maze.solve(my_maze)


if __name__ == '__main__':
    main(sys.argv[1:])

''' testing

if __name__ == '__main__':
    f = open("small_maze.txt", 'r', encoding='utf-8')
    g = [line.splitlines() for line in f.readlines()]

    for y, x in enumerate(g):
        if x[0][0] == ' ':
            start = (0, y)

    for y, x in enumerate(g):
        if x[0][-1] == ' ':
            end = (len(x[-1]) - 1, y)


    visited = [start]
    exploring = [visited]
    while end not in visited:
        current_path = []
        current_path.append(exploring.pop())
        current_cord = current_path[-1]
        if current_cord == end:
            print(current_path)
        (w, z) = current_cord[0]
        for y, x in enumerate(g):
            print(g[z][w][w+1])
'''