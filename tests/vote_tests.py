import sys

from nose.tools import raises

from verify_vote import determine_winner
from verify_vote import NoCandidatesLeftError
from verify_vote import TooManyRoundsError


def test_a_wins():
    assert 'a' == determine_winner([('a', 'b', 'c'),
                                    ('b', 'a', 'c'),
                                    ('a', 'c', 'b'),
                                    ('b', 'c', 'a'),
                                    ('a', 'c', 'b'),
                                    ('b', 'c', 'b'),])
    
def test_a_wins2():
    assert 'a' == determine_winner([('a', 'b'),
                                    ('a', 'b')])

def test_eliminate_two():
    assert 'a' == determine_winner([('a', 'b'),
                                    ('a', 'c')])
    expected_output = """These names received at least one vote:
  a, c, b

Round 1
voting for b
voting for c
eliminated this time: c, b

We have a winner: a"""

    actual = sys.stdout.getvalue().strip()
    assert actual == expected_output

@raises(NoCandidatesLeftError)
def test_no_one_left():
    determine_winner([('a', 'b'),
                      ('c', 'd')])

    
