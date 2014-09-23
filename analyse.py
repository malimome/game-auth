from __future__ import division
import pdb

class Analyser():
  def __init__(self):
    pass

  #d is the scores for one ref user
  #allusers is the set of all users
  def getMinRes(d, allusers):
    min_value = min(d.itervalues())
    min_keys = [allusers.index(k) for k in d if d[k] == min_value]
    mind = 1000000
    for val in d.values():
      diff = abs(min_value - val)
      if diff == 0:
        continue
      if mind > diff:
        mind = diff
    return min_keys, mind

  def analyseResultUser(self, refuser, scores):
    sorted_scores = sorted(scores.itervalues())
    rank = 0
    for i in sorted_scores:
      if scores[refuser] > i:
        rank += 1
    return rank

  def calcPercent(self, refuser, scores):
    numOfUsers = len(scores)
    rank = self.analyseResultUser(refuser, scores)
    selfdist = scores[refuser]
    percent1 = float(numOfUsers-rank*2)/numOfUsers
    percent2 = 1-selfdist
    res = 0.9*percent1 + 0.1*percent2
    #res = percent1
    return res

