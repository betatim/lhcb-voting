import sys
import csv
import operator
from collections import Counter
from itertools import chain


def load_votes(fname="election.csv"):
    votes = []
    with open(fname) as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            votes.append(line[1:])

    # slice off the header
    return votes[1:]

def valid_token(valid_tokens, ballot):
    return ballot[0] in valid_tokens

def unspoilt_ballot(ballot):
    return len(ballot) == len(set(ballot))

def remove_multi_voters(ballots):
    vote_counts = Counter(ballot[0] for ballot in ballots)
    valid_ballots = {}
    for ballot in ballots:
        token = ballot[0]
        # if someone votes more than once all their votes
        # get removed
        if token not in valid_ballots:
            valid_ballots[token] = ballot
        else:
            valid_ballots.pop(token)

    return valid_ballots.values()

def count_votes(rankings, eliminated=set()):
    votes = []
    for ranking in rankings:
        # vote for lowest ranked person,
        # not yet eliminated
        for person in reversed(ranking):
            if person not in eliminated:
                print 'voting for', person
                votes.append(person)
                break
            
    counts = Counter(votes)
    ranking = sorted(counts.iteritems(),
                     key=operator.itemgetter(1),
                     reverse=True)

    # Everyone who received the same number
    # of votes as the least popular person
    # is eliminated
    eliminees = [ranking[0][0]]
    threshold_vote = ranking[0][1]
    for name,votes_ in ranking[1:]:
        if votes_ == threshold_vote:
            eliminees.append(name)
            
    return set(eliminees)


class NoCandidatesLeftError(Exception):
    pass

class TooManyRoundsError(Exception):
    def __init__(self, remaining):
        self.remaining = remaining


def determine_winner(ballots):
    ballots = list(ballots)

    names = set(chain(*ballots))
    print "These names received at least one vote:"
    print "  " + ", ".join(names)
    
    eliminated = set()
    rounds = 1
    
    while True:
        print
        left_over = [name for name in names if name not in eliminated]
        if len(left_over) == 1:
            print "We have a winner:", left_over[0]
            return left_over[0]

        print "Round %i"%rounds
        eliminated_ = count_votes(ballots, eliminated)
        print "eliminated this time:", ", ".join(eliminated_)
        
        eliminated = eliminated.union(set(eliminated_))

        left_over = [name for name in names if name not in eliminated]
        if len(left_over) == 0:
            print "Something went wrong"
            print "Everyone has been eliminated"
            raise NoCandidatesLeftError()
            
        rounds += 1
        
        if rounds > 50:
            print "Something went wrong"
            print "After 50 rounds of voting no winner could be found"
            print 'left over', left_over
            raise TooManyRoundsError(left_over)


if __name__ == "__main__":
    votes = load_votes()
    print "Loaded a total of %i ballots"%(len(votes))

    valid_ballots = filter(unspoilt_ballot, votes)
    print "Unspoilt ballots %i"%(len(valid_ballots))

    valid_ballots = remove_multi_voters(valid_ballots)
    print "Single vote ballots %i"%(len(valid_ballots))

    VALID_TOKENS = set(line.strip()
                   for line in open("valid_tokens.txt").readlines())
    valid_token_ = lambda x: valid_token(VALID_TOKENS, x)
    valid_ballots = filter(valid_token_, valid_ballots)
    print "Valid token ballots %i"%(len(valid_ballots))
    
    if not valid_ballots:
        print "No valid ballots left."
        sys.exit(1)

    determine_winner(ballot[1:] for ballot in valid_ballots)

