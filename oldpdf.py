import pdb
from base import features, enfeatures, dtlength, dttestlength
import base


class ClassificationPDF(base.ClassificationBase):
  def genSpaceProb(self, udata):
    udlen = len(udata)
    ind = []
    ftnum = []
    pdb.set_trace()
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

  def getDistance(self, usersp, clssp):
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

  def classifyUsers(self):
    users = self.getUsers()
    for usertest in users:
      clsfydt = self.getUserData(self.dtpath + usertest, dtlength, dttestlength)[0]
      clsftsp = self.genSpaceProb(clsfydt)
      if len(clsfydt) < dttestlength:
        continue;
      #print "----- Testing user-> @@@ %s @@@ with test length: %d"%(usertest, len(clsfydt))
      dist = {}
      for user in users:
        userdt = self.getUserData(self.dtpath + user, 0, dtlength)[0]
        usersp = self.genSpaceProb(userdt)
        dist[user] = self.getDistance(usersp, clsftsp)
        #print "Distance for User: %s, len: %d, dist: %d"%(user, len(userdt), dist[user])

      minval = min(val for val in dist.values())
      minusers = [user for user in dist.keys() if dist[user] == minval]
      print "%s ->  %s "%(usertest, str(minusers))  # print user with min distance

  def frange(self, start,stop, step=1.0):
      while stop > start:
          yield stop
          stop -=step

  def getWeights(self, users):
    sp = {}
    data = {}
    for user in users:
      data[user] = self.getUserData(dtpath + user, 0, dtlength)[0]
      if len(data[user]) < dtlength-1:
        print "Problem in user data %s with len %d"%(user,len(data[user]))

    for ft in features:
      enfeatures = [ft] 
      ftmax = 0
      maxofft = 0
      for i in frange(features[ft]['sts'], features[ft]['ste'],features[ft]['stt']):
        features[ft]['step'] = i
        for user in users:
          sp[user] = self.genSpaceProb(data[user])
        
        f = lambda x,y: self.getDistance(sp[x], sp[y])
        dist = 0
        for pair in itertools.combinations(users,2):
          dist += f(*pair)
        if dist > ftmax:
          ftmax = dist
          maxofft = i
      print "Feature %s has max on step %f"%(features[ft]['name'],i)



