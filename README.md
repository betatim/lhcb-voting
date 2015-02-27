# lhcb-voting

One stop shop for running an election over the web

This implements the election procedure used at
the LHCb experiment.

The election is fairly anonymous. The result can
be verified by every participant, the integrity
of the election relies on a large fraction of
voters checking that their vote was counted
correctly.


# Setting up an Election

To start a new election, create a google form like
[this one](https://docs.google.com/forms/d/1exEzNZVcNa3o4KL4CpJrOPfU84_rZKzvj7sMI4L3sIQ/viewform)

You need a field to enter the token, as well as
several multiple choice fields listing the
candidates. Your form should produce a results
spreadsheet similar to
[this one](https://docs.google.com/spreadsheets/d/1FUIG6S118rKZPwJsqSpWW9eZGn67lHdk8MyeJd2agRc/edit?usp=sharing).

Then edit `send_ballots.py` to include the email
addresses of all eligible voters, as well as
modifying the text of the email, link to the form,
etc, etc.

Afterwards run it, it will send one email to each
voter with instructions for them.

It will create a file named `valid_tokens.txt`
make sure to keep a copy as it will be needed
to verify the election and compute the result.


# Counting the Votes

Once the election has finished, download the
results spreadsheet as CSV from Google Drive and
name it `election.csv`. Place it in the directory
together with `verify_election.py` and
`valid_tokens.txt`. To count the votes run
`verify_election.py`. It will print the winner
of each round, as well as the overall winner.

It will perform at most 50 rounds of elimination
and stop if there is no winner by that time.


# Technical Details

To come, for the moment simply read the code.
