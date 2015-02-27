import csv
import operator
from collections import Counter


# This produces a tie
votes = [("b6a08f2fe68f3e1be8dbabcbd0abf3e497752a08c9365ba4009c85e7d3d21879",
          "John", "Jane", "Alice", "Joe"),
         ("aaea5ddf7712c351f57de1381f05734b408e39f86dbd60ba4d54446eebca202c",
         "Joe", "John", "Jane", "Alice"),
         # double voter
         ("d5384124fdb6f8c7636c7d25015d536a4b93f0b2a380d64bab566b69cb9f9199",
          "John", "Jane", "Alice", "Joe"),
         ("d5384124fdb6f8c7636c7d25015d536a4b93f0b2a380d64bab566b69cb9f9199",
          "John", "Jane", "Alice", "Joe"),
         # invalid token
         ("e5384124fdb6f8c7636c7d25015d546a4b93f0b2a380d64bab566b69cb9f9199",
          "John", "Jane", "Alice", "John")
]
# john wins
votes = [("b6a08f2fe68f3e1be8dbabcbd0abf3e497752a08c9365ba4009c85e7d3d21879",
          "John", "Jane", "Alice", "Joe"),
         ("aaea5ddf7712c351f57de1381f05734b408e39f86dbd60ba4d54446eebca202c",
         "Joe", "John", "Jane", "Alice"),
         ("d5384124fdb6f8c7636c7d25015d536a4b93f0b2a380d64bab566b69cb9f9199",
          "John", "Jane", "Alice", "Joe"),
]

def load_votes(fname="election.csv"):
    votes = []
    with open(fname) as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            votes.append(line[1:])

    # slice off the header
    return votes[1:]

VALID_TOKENS = set(line.strip()
                   for line in open("valid_tokens.txt").readlines())
def valid_token(ballot):
    return ballot[0] in VALID_TOKENS

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
        for person in ranking:
            if person not in eliminated:
                votes.append(person)
                break
            
    counts = Counter(votes)
    ranking = sorted(counts.iteritems(),
                     key=operator.itemgetter(1), reverse=True)

    winners = [ranking[0]]
    eliminees = []
    for name,votes in ranking[1:]:
        if votes == winners[-1][1]:
            winners.append((name, votes))

        else:
            eliminees.append(name)

    tie = len(winners) > 1
    print "{win} of this round:".format(win="Winners" if tie else "Winner")
    for winner in winners:
        print "Winner: %s with %i votes"%(winner)
        
    return tie, winners[0], eliminees

def determine_winner(ballots):
    ballots = list(ballots)
    
    eliminated = set()
    rounds = 1
    while True:
        print
        print "Round %i"%rounds
        is_tied, winner, eliminated = count_votes(ballots, eliminated)
        # if no one got eliminated, we have a winner
        if not eliminated and not is_tied:
            print
            print "The overall winner:", winner[0]
            break

        elif not eliminated and is_tied:
            print
            print "There is a tie and no one was eliminated in the last round"
            break
    
        eliminated = set(eliminated)
        rounds += 1
        
        if rounds > 50:
            print "Something went wrong"
            print "After 50 rounds of voting no winner could be found"
            break


votes = load_votes()
valid_ballots = filter(unspoilt_ballot, votes)
valid_ballots = remove_multi_voters(valid_ballots)
valid_ballots = filter(valid_token, valid_ballots)

determine_winner(ballot[1:] for ballot in valid_ballots)
