from verify_vote import determine_winner

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

    
