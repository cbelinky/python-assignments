import sys
class Ballot:
    """ A class that can find unique items out of multiple word lists.
    
    Attributes:
        votes (dict of str: int): each key is a name of a candidate; each value is
            the candidate's score.
    """
    def __init__(self, vote_str):
        """passes a ballot and stores the result in votes attribute
        
        Arguments:
            vote_str {[string]} -- [a string consisting of candidates and scores]
        """
        self.votes = self.parse_votes(vote_str)

    def parse_votes(self, vote_str):
        """builds a dictionary where the keys are candidate names and the values are the scores assigned to those candidates, as integers
        
        Arguments:
            vote_str {[string]} -- [a string consisting of candidates and scores]
        
        Returns:
            [dictionary] -- [ keys are candidate names and the values are the scores assigned to those candidates, as integers]
        """
        parsed_votes = {}
        for vote in vote_str:
            i = vote.split(':')
            parsed_votes[i[0]] = int(i[1])
        return parsed_votes

    def preference(self, candidate1, candidate2):
        """This method determines if the ballot shows a preference for either of the two candidates passed as arguments
        
        Arguments:
            candidate1 {[str]} -- [ the name of one candidate ]
            candidate2 {[str]} -- [ the name of one candidate ]
        
        Returns:
            [str] -- [ the name of one candidate ]
        """
        if candidate1 > candidate2:
            return candidate1
        elif candidate1 < candidate2:
            return candidate2
        else:
            return None

def read_ballots(path):
    """[open the specified file for reading and creates an instance of the Ballot class containing the scores specified on the line]
    
    Arguments:
        path {[str]} -- [a path to a text file containing one ballot per line]
    
    Returns:
        [list] -- [list of all the Ballot objects it created]
    """
    ballots = []
    f = open(path, 'r', encoding='utf-8')
    for line in f:
        x = line.split(',')
        ballots.append(Ballot(x))
    return ballots


def find_winner(ballots):
    """[evaluates each ballot and counts the number of times each candidate won a ballot, returning the candidate with the most ballots won.]
    
    Arguments:
        ballots {[list]} -- [list of ballot objects]
    
    Returns:
        [str] -- [name of winning candidate]
    """
    winners = []
    counts = {}
    for ballot in ballots:
        most_votes = sorted(ballot.votes, key=ballot.votes.get, reverse=True)[:2]
        candidate1 = ballot.votes[most_votes[0]]
        candidate2 = ballot.votes[most_votes[1]]
        winner = ballot.preference(candidate1, candidate2)
        if winner == candidate1:
            winners.append(most_votes[0])
        elif winner == candidate2:
            winners.append(most_votes[1])
        else:
            winners.append(None)
    for candidate in winners:
        counts[candidate] = counts.get(candidate, 0) + 1
    counts = sorted(counts, key=counts.get, reverse=True)[:2]
    if counts[0] == None:
        return counts[1]
    else:
        return counts[0]

def main(path):
    """[calls read_ballots() to create a list of ballot objects containing the data from the text file, passes this list to find_winner() and print the result to the console.]
    
    Arguments:
        path {[str]} -- [path to text file containing one ballot per line.]
    """
    ballots = read_ballots(path)
    print(find_winner(ballots))


if __name__ == '__main__':
    main(sys.argv[1:])