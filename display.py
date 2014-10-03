import numpy as np
import string
import pdb
import analyse

#Input is the result containing all scores with a refuser
# This function will print the results based on a threshold distance from all users.
def newdisplay(refscores, profiles):
  WARN = '\033[91m'
  END = '\033[0m'
  AllY = 0
  um = ""
  usermap = ""
  rs = ""
  resultstr = ""
  print("Number of users in experiment: \t%d"%len(refscores))
  print("------------------------------------")
  allusers = refscores.keys()
  flag = 0
  #pdb.set_trace()
  for refuser in allusers:
    an = analyse.Analyser()
    perc,rank = an.calcPercent(refuser, refscores[refuser])
    userind = str(allusers.index(refuser))
    um = string.ljust(userind, 4) + "-> " + string.ljust(refuser[:20], 22) + " | "
    rs = string.ljust(userind, 3) + " -> "
    rs += string.ljust(str(perc)[0:5], 6)
    rs += string.ljust(str(rank), 2)
 #   rs += string.ljust(str(uave[refuser])[0:4], 5) 
 #   rs += string.ljust(str(umiss[refuser]), 5)
    if perc >= 0.9:
      rs += string.ljust("Y", 2)
      AllY += 1
    else:
      rs = WARN + rs + string.ljust("N", 2) + END
      um = WARN + um + END
    rs += string.ljust("|", 5)
    resultstr += rs
    usermap += um
    if flag == 2:
      resultstr += "\n"
      usermap += "\n"
    flag = (flag + 1) % 3
  print usermap + "\n"
  print resultstr
  print("------------------------------------")
  print("\n%d out of %d of users were accepted."%(AllY, len(allusers)))

#  getStats(result, ud_ftlevel, level)
#  allusers = sorted(result.iterkeys(), key = lambda user: 4*uave[user] + umiss[user])
  
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

def display_result(result):
  score = 0 #score of the method for all users
  minscore = 0 #min score in distance for all
  print("Number of users in experiment: \t%d"%len(result))
  print("------------------------------------")
  flag = 0
  allusers = sorted(result.iterkeys())
  for refuser in allusers:
    d = result[refuser]
    min_keys, mind = getMinRes(d, allusers)
    if allusers.index(refuser) in min_keys:
      score += 1.0/(len(min_keys)*len(result))
      minscore += mind
    else:
      minscore += mind * 3
#    print("%28s -> %28s\t\t"%(refuser, str(min_keys))),
    print string.ljust(str(allusers.index(refuser)), 3), " -> ", string.ljust(str(min_keys), 15), 
    if flag == 2:
      print ""
    flag = (flag + 1) % 3
  print("\n------------------------------------")
  print("score: %f and minscore:%f"%(score, minscore))

uave = {}
umiss = {}

def getStats(result, udftlevel, level):
  for user in result:
    ftlevel = udftlevel[user]
    ydiffs = np.array(ftlevel[2])
    umiss[user] = sum(ftlevel[7])
    absyd =  np.absolute(ydiffs)
    uave[user] = np.mean(absyd)
    ysdev    = np.std(absyd) # stdev should compute from 0 not mean


