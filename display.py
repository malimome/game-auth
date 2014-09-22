import numpy as np
import string
import pdb

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


def getMinVrf(d, allusers, refuser):
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

#Input is the result containing all scores with a refuser
# This function will print the results based on a threshold distance from all users.
def display_vrf(result, ud_ftlevel, level):
  global uave, umiss
  WARN = '\033[91m'
  END = '\033[0m'
  print("Number of users in experiment: \t%d"%len(result))
  print("------------------------------------")
  print("uind -> udist Y/N #ufacc uave umiss")
  flag = 0
  zeta = 0.65
  getStats(result, ud_ftlevel, level)
  allusers = sorted(result.iterkeys(), key = lambda user: 4*uave[user] + umiss[user])
  AllY = 0
  um = ""
  usermap = ""
  rs = ""
  resultstr = ""
  for refuser in allusers:
    d = result[refuser]
    ds = sorted(d.itervalues())
    zeta = ds[2]
    userind = str(allusers.index(refuser))
    um = string.ljust(userind, 4) + "-> " + string.ljust(refuser[:20], 22) + " | "
    rs = string.ljust(userind, 3) + " -> "
    rs += string.ljust(str(d[refuser])[0:5], 6)
    #min_keys = [allusers.index(k) for k in d if d[k] <= zeta]
    min_keys = [allusers.index(k) for k in d if d[k] <= d[refuser]]
    rs += string.ljust(str(len(min_keys)-1), 4)
    rs += string.ljust(str(uave[refuser])[0:4], 5) 
    rs += string.ljust(str(umiss[refuser]), 5)
    if d[refuser] <= zeta:
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

  
def getMaxRes(d, allusers):
  max_value = max(d.itervalues())
  max_keys = [allusers.index(k) for k in d if d[k] == max_value]
  maxd = 0
  for val in d.values():
    diff = abs(max_value - val)
    if diff == 0:
      continue
    if maxd < diff:
      maxd = diff
  return max_keys, maxd

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
    #min_keys, mind = getMinRes(d, allusers)
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


