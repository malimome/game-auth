import data as mldata
import pdb

class ClassificationBase(object):
  def __init__(self, start, length):
    self.start = start
    self.length = length
    self.userlvl = dict()
    self.ud,self.mincLF = self.readProfiles()  #ud is the user data per level feature
    self.ulf = dict() #the training data
    self.ulftest = dict()   # the test data
    self.level = -1
    #weights = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    self.weights = [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]
    #weights = [0.65, 0.6, 0.55, 0.5, 0.5, 0.3, 0.3, 0.2]

  def checkGenSplitData(self, level, feature = -1):
    ud = self.ud
    if level != self.level:
      self.ulf, self.ulftest = self.getSplitData(level)
      self.level = level
      return True
    if not self.ulf or not self.ulftest:
      self.ulf, self.ulftest = self.getSplitData(level)
    for user in self.userlvl[level]:
      if user not in self.ulf or user not in self.ulftest:
        print ("Prob in data for user %s"%user)
        return False
      if feature != -1:
        if not self.ulf[user][feature] or not self.ulftest[user][feature]:
          print("Prob for level %d data, feature %d user %s"%(level, feature, user))
          return False
      else:
        for feature in mldata.enfeatures:
          if not self.ulf[user][feature] or not self.ulftest[user][feature]:
            print("Prob for level %d data, feature %d user %s"%(level, feature, user))
            return False
    return True

  def classifyByFeature(self, feature):
    levelscores = {}
    for level in self.ud.ftlevels:
      levelscores[level] = self.classifyByLevelFeature(level, feature)

  def classifyUsers(self):
    allscores = {}
    for level in mldata.levelenum:
      allscores[level] = self.classifyByLevel(level)
    return allscores

  def getSplitData(self, level):
    ud = self.ud
    ulf = dict()
    ulftest = dict()
    maxlevel = self.mincLF[level]
    if mldata.dtmaxlen[level] != 0 and mldata.dtmaxlen[level] < maxlevel:
      maxlevel = mldata.dtmaxlen[level]
    if mldata.DEBUGL >= 1:
      print("Number of rows of data \t\t %d"%maxlevel)
      print("Level of the game \t\t %d"%level)
    for user in self.userlvl[level]:
      ulf[user] = {}
      ulftest[user] = {}
      for feature in mldata.enfeatures:
        data = ud[user][level][feature]
        data = data[-maxlevel:] # TODO change the slice to pick
        #data = data[:maxlevel]
        test,dt = self.splitTestTraining(data, self.start, self.length)
        ulf[user][feature] = dt
        ulftest[user][feature] = test
    return ulf, ulftest

  def splitTestTraining(self, data, start, length):
    dtlen = len(data)
    if abs(length)*3 > dtlen:
      return [],[]
    end = (start + length) % (dtlen)
    a3 = list()
    a4 = list()
    if end==0:
      a3 = data[start:]
      a4 = data[:start]
    elif start == 0 and length<0:
      a3 = data[end:]
      a4 = data[:end]
    elif end > start: 
      a3 = data[start:end]
      a4 = data[:start]+data[end:]
    else:
      a3 = data[:end]+data[start:]
      a4 = data[end:start]
    return a3,a4

  def readProfiles(self):
    """ Get data for all users + the min in each level for all users """
    users = mldata.getUsers()
    ud = {}
    udcount = {}
    mincountperL = {}
    for user in users:
      dtuser = mldata.UserData(user)
      udcount[user] = dtuser.getUserFeatureLevels()
      ud[user] = dtuser.ftlevels #data from all levels and features for one user

    for level in mldata.levelenum:
      minc = 1000000
      self.userlvl[level] = []
      for user in users:
        if mldata.DEBUGL >= 2:
          print ("User %s, Level %d -> Length:%d"%(user,level,udcount[user][level]))
        cntuserlvl = udcount[user][level]
        if cntuserlvl <= 120:
          continue
        self.userlvl[level].append(user)
        if udcount[user][level] < minc:
          minc = udcount[user][level]
      mincountperL[level] = minc
    return ud, mincountperL

class ClassificationOneD(ClassificationBase):
  def __init__(self, start, length):
    super(ClassificationOneD, self).__init__(start, length)

  def classifyByLevelFeature(self, level, feature):
    if not self.checkGenSplitData(level, feature):
      return {}
    refscores = {}
    for ref in self.userlvl[level]:
      refscores[ref] = self.classifyByLevelFeatureRef(level, feature, ref)
    return refscores
   
  def classifyByLevel(self, level):
    featurecores = {}
    if not self.checkGenSplitData(level):
      return {}
    for ft in mldata.enfeatures:
      featurecores[ft] = self.classifyByLevelFeature(level, ft)
    return featurecores
  
class ClassificationMultiD(ClassificationBase):
  def __init__(self, start, length):
    super(ClassificationMultiD, self).__init__(start, length)
 
  def classifyByLevelFeature(self, level, feature = -1):
    if not self.checkGenSplitData(level):
      return {}
    refscores = {}
    for ref in self.userlvl[level]:
      refscores[ref] = self.classifyByLevelMultiRef(ref)
    return refscores  

  def classifyByLevelUser(self, level, user):
    if not self.checkGenSplitData(level):
      return {}
    scores = self.classifyByLevelFeature(level)
    return scores
 
  def classifyByLevel(self, level):
    if not self.checkGenSplitData(level):
      return {}
    scores = self.classifyByLevelFeature(level)
    return scores
   
class ClassificationFusion(ClassificationMultiD):
  def __init__(self, start, length):
    super(ClassificationFusion, self).__init__(start, length)

  def classifyByLevelMultiRef(self, ref):
    scores = {}
    for ft in mldata.enfeatures:
      scores[ft] = self.classifyByLevelFeatureRef(self.level, ft, ref)

    finalscores = {}
    for user in self.userlvl[self.level]:
      finalscores[user] = 0
      for ft in mldata.enfeatures:
        finalscores[user] += scores[ft][user] * self.weights[ft]
    return finalscores

