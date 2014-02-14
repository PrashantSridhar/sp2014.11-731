#!/opt/local/bin/python

import optparse
import sys


def viterbi(trans_p, start_p, emit_p, target, source):
    V = [{}]
    paths = {}
 
    # Initialize base cases (t == 0)
    for y in source:
        V[0][y] = start_p[y] * emit_p[y][target[0]]
        paths[y] = [y]
 
    # alternative Python 2.7+ initialization syntax
    # V = [{y:(start_p[y] * emit_p[y][obs[0]]) for y in states}]
    # path = {y:[y] for y in states}
 
    # Run Viterbi for t > 0
    for t in range(1, len(target)):
        V.append({})
        newpaths = {}
 
        for y in source:
            (prob, state) = max((V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in source)
            V[t][y] = prob
            newpaths[y] = paths[state] + [y]
 
        # Don't need to remember the old paths
        paths = newpaths

    (prob, state) = max((V[t][y], y) for y in states)
    return (prob, paths[state])


def EM(source_corpus, target_corpus):
  
