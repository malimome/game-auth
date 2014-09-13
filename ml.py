from os import listdir
from os.path import isfile, join, isdir
import itertools
import sys
import pdb
import matplotlib.pyplot as plt
import random
import colorsys


features = {
            0: {'start': 0, 'end': 20, 'step': 0.5, 
              'func': lambda x: float(x[8]), 'enabled': 1, 'name': 'shoottime', 
              'sts': 0.1, 'ste': 2.0, 'stt': 0.1},
            1: {'start': -120, 'end': 120, 'step': 20, 
              'func': lambda x: float(x[7])-float(x[5]), 'enabled': 1, 'name':'ydiff',
              'sts': 1, 'ste': 30, 'stt': 1},
            2: {'start': 3, 'end': 7.8, 'step': 0.3, 
              'func': lambda x: float(x[11]), 'enabled': 1, 'name': 'velocity',
              'sts': 0.05, 'ste': 0.5, 'stt': 0.05},
       }

enfeatures = [d for d in features if features[d]['enabled']==1] 
level = '0'
condition = lambda x: (x[9].strip() == level)
dtmaxlen = [[200, 20], [110,20], [],[],[],[],[200,30]]
dtlength = dtmaxlen[int(level)][0]
dttestlength = dtmaxlen[int(level)][1]

dtpath = "../raw/"
def getUsers():
  global dtpath
  if not isdir(dtpath):
    dtpath = "./"
  blacklist = ["FK__123.csv", "MMS__1362.csv", "AmirT__123.csv", "AH__1234.csv"]#, "User1__123.csv"]
  users = [ f for f in listdir(dtpath) if (f.endswith(".csv") and isfile(join(dtpath,f)) and f not in blacklist)]
  if len(users)==0:
    print "No user files, please put the files in current directory."
    exit(0)
  return users

def getUserData(dtfile, start=0, length=10000):
  dtcount = 0
  udata = []
  for line in open(dtfile):
    if dtcount == 0:
      dtcount += 1
      continue
    line = line.strip()
    data= line.split(",")
    #check condition for level
    if condition(data):
      dtcount += 1
      if start <= dtcount:
        tmp = []
        for ft in enfeatures:
          tmp.append(features[ft]['func'](data))
        udata.append(tmp)
      else:
        continue
      if dtcount >= length + start:
        break
  return udata, dtcount

def genSpaceProb(udata):
  udlen = len(udata)
  ind = []
  ftnum = []
  for ft in enfeatures:
    ftnum.append(float(features[ft]['end'] - features[ft]['start'])/features[ft]['step'])
  maxasbase = max(ftnum) + 1
  numrows = 0
  space = {} # keeps the sparse matrix of probabilities for user
  for row in udata:
    index = 0
    numrows += 1
    for ft in enfeatures:
      rowft = int((row[ft] - features[ft]['start'])/features[ft]['step'])  # actual value - base / len
      if rowft < 0:
        rowft = 0
      index += rowft * pow(maxasbase, ft)  #find the unique index keeping the distacce 
    if index not in space:
      space[index] = 1
    else:
      space[index] += 1 
  return space

def getDistance(usersp, clssp):
  # union of indexes of usersp and clssp
  keyunion = list(set(usersp.keys()) | set(clssp.keys()))
  diffscore = 0
  for index in keyunion:
    if index in usersp and index in clssp:
      diffscore += abs(usersp[index] - clssp[index])
    elif index in usersp and index not in clssp:
      diffscore += usersp[index] 
    elif index not in usersp and index in clssp:
      diffscore += clssp[index] 
  return diffscore

def getlvlLength(users):
  for user in users:
    dt = getUserData(dtpath + user, 150000, 20)
    print "Length for user %s is %d"%(user,dt[1])

def classifyUsers(users):
  for usertest in users:
    clsfydt = getUserData(dtpath + usertest, dtlength, dttestlength)[0]
    clsftsp = genSpaceProb(clsfydt)
    if len(clsfydt) < dttestlength:
      continue;
    #print "----- Testing user-> @@@ %s @@@ with test length: %d"%(usertest, len(clsfydt))
    dist = {}
    for user in users:
      userdt = getUserData(dtpath + user, 0, dtlength)[0]
      usersp = genSpaceProb(userdt)
      dist[user] = getDistance(usersp, clsftsp)
      #print "Distance for User: %s, len: %d, dist: %d"%(user, len(userdt), dist[user])

    minval = min(val for val in dist.values())
    minusers = [user for user in dist.keys() if dist[user] == minval]
    print "%s ->  %s "%(usertest, str(minusers))  # print user with min distance

def frange(start,stop, step=1.0):
    while stop > start:
        yield stop
        stop -=step

def getWeights(users):
  sp = {}
  data = {}
  for user in users:
    data[user] = getUserData(dtpath + user, 0, dtlength)[0]
    if len(data[user]) < dtlength-1:
      print "Problem in user data %s with len %d"%(user,len(data[user]))

  for ft in features:
    enfeatures = [ft] 
    ftmax = 0
    maxofft = 0
    for i in frange(features[ft]['sts'], features[ft]['ste'],features[ft]['stt']):
      features[ft]['step'] = i
      for user in users:
        sp[user] = genSpaceProb(data[user])
      
      f = lambda x,y: getDistance(sp[x], sp[y])
      dist = 0
      for pair in itertools.combinations(users,2):
        dist += f(*pair)
      if dist > ftmax:
        ftmax = dist
        maxofft = i
    print "Feature %s has max on step %f"%(features[ft]['name'],i)

if len(sys.argv) == 3:
  level = sys.argv[2].strip()
if len(sys.argv) <= 1:
  print "Problem in command line: python ml.py <class|weight|length> <level=0 to 7>"
  print "Classify data for level 0: python ml.py class 0"
  exit(0)
if len(sys.argv) <= 1:
  classifyUsers(getUsers())
elif sys.argv[1] == "class":
  classifyUsers(getUsers())
elif sys.argv[1] == "weight":
  getWeights(getUsers())
elif sys.argv[1] == "length":
  getlvlLength(getUsers())
else:
  print "problem"


