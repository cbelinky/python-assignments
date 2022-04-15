### ASSIGNMENT INSTRUCTIONS
For this homework assignment you will write a program that can read in a maze constructed from text characters and find a path through that maze.

The maze file consists of multiple newline-terminated lines of text; each line of text should have the same number of characters. You will convert this text into a list of strings, stripping newlines off the end of each line and discarding any blank lines. The index of each string in the list can be thought of as a y coordinate; the index of each character in a string can be thought of as an x coordinate. All non-space characters in the maze represent walls; you may not pass through a wall. Your job is to generate a list of sequential (x, y) coordinate tuples representing the shortest path through the maze. In the case of the maze above, that path is:

[(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (6, 5)]

For this assignment, we will assume that the maze has exactly one opening on the left side, which will be the starting point, and exactly one opening on the right side, which will be the ending point.

### Solving a maze
We can solve a maze by starting at the start of the maze and checking every possible move that takes us somewhere we haven't been before until we reach the end of the maze. As we explore the maze, we will want to keep track of the path that got us from the start to whatever point we are currently at; that way, when we reach the end, we will know how we got there. Each time we reach a fork in the maze, there will be multiple possible paths we can take. We can make a list of all possible paths that we know about and explore them one at a time until we reach the end.

We will want to keep track of the following things:

the coordinates we have already visited, so that we don't go in circles; this should be a list of tuples of the form (x, y); initially, this will be a list containing only our starting point
the paths we are currently exploring; this should be a list of lists of tuples of the form (x, y); initially, this will be a list containing our starting path, which is a list containing only our starting point
We can use the following algorithm to find a path through the maze:

WHILE there are paths to explore:
take one of the paths and remove it from the list of paths (let's call this the current path)
look at the last coordinate in that path; it is the farthest point on that path that we know how to get to (let's call this the current coordinate)
IF the current coordinate is the end of the maze:
Success! RETURN the current path
FOR EACH of the positions left of, right of, above, and below the current coordinate:
IF the position in question is in the maze AND the position in question is a space character AND we have not yet visited the position in question:
add the position to the list of coordinates we have visited
make a copy of the current path (don't modify the current path directly; lists are mutable!) and add the new position to the end; add this new path to the list of paths we are currently exploring
