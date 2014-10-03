import data as mldata
import pdb

class ClassificationBase(object):
  def __init__(self, start, length):
    self.start = start
    self.length = length
    self.profiles = {}
    self.attempt = {}
    self.userlvl = []
    self.mindtPr = {}
    self.level = -1

  def readProfiles(self):
    """ Get data for all users + the min in each level for all users """
    users = mldata.getUsers()
    ud = {}
    udcount = {}
    mincountperL = {}
    for user in users:
      dtuser = mldata.UserData(user, self.level)
      udcount[user] = dtuser.getUserFeatureLevels()
      ud[user] = dtuser.ftlevels #data from all levels and features for one user

    minc = 1000000
    self.userlvl = []
    for user in users:
      if mldata.DEBUGL >= 2:
        print ("User %s, Level %d -> Length:%d"%(user,self.level,udcount[user]))
      cntuserlvl = udcount[user]
      if cntuserlvl <= 109:
        continue
      self.userlvl.append(user)
      if udcount[user] < minc:
        minc = udcount[user]
    if minc == 1000000:
      minc = 0
    mincountperL = minc
    return ud, mincountperL

  def readAttempt(self, level, user):
    users = mldata.getUsers(is_profile = False)
    if user not in users:
      return False, False
    dtuser = mldata.UserData(user, self.level, is_profile = False)
    udcount = dtuser.getUserFeatureLevels()
    return dtuser.ftlevels,udcount

  def readPAdata(self, level, user=''):
    self.level = level
    if not self.profiles:
      self.profiles,self.mindtPr = self.readProfiles()
    if user=='':
      return True
    self.attempt, tmp = self.readAttempt(level, user)
    if tmp < 30:
      print "0"
      print "0"
      print("Not enough data for login. At least 30 rounds of game is needed but %d is provided!"%tmp)
      exit(0)

  def classifyByFeature(self, feature):
    levelscores = self.classifyByLevelFeature(level, feature)

  def classifyUsers(self):
    allscores = {}
    for level in mldata.levelenum:
      allscores[level] = self.classifyByLevel(level)
    return allscores

class ClassificationOneD(ClassificationBase):
  def __init__(self, start, length):
    super(ClassificationOneD, self).__init__(start, length)

  def classifyByLevelFeature(self, level, feature):
    if not self.readPAdata(level):
      return {}
    refscores = {}
    for ref in self.userlvl:
      refscores[ref] = self.classifyByLevelFeatureRef(level, feature)
    return refscores
   
  def classifyByLevel(self, level):
    featurecores = {}
    if not self.readPAdata(level):
      return {}
    for ft in mldata.enfeatures:
      featurecores[ft] = self.classifyByLevelFeature(level, ft)
    return featurecores
  
class ClassificationMultiD(ClassificationBase):
  def __init__(self, start, length):
    super(ClassificationMultiD, self).__init__(start, length)
 
  def classifyByLevelFeature(self, level, user = ''):
    #if not self.readPAdata(level):
    #  return {}
    refscores = {}
    if user != '':
      return self.classifyByLevelMultiRef(user)

    for ref in self.userlvl:
      refscores[ref] = self.classifyByLevelMultiRef(ref)
    return refscores  

  def classifyByLevelUser(self, level, user):
    pdb.set_trace()
    cnt = self.readPAdata(level, user)
    if mldata.DEBUGL >=2:
      print("User login data length: %d"%cnt)
    if cnt < 30:
      return {}

    self.level = level
    scores = self.classifyByLevelFeature(level, user)
    return scores
 
  def classifyByLevel(self, level):
    scores = {}
    self.level = level
    if not self.profiles:
      self.profiles,self.mindtPr = self.readProfiles()
    for user in self.userlvl:
      sc = self.classifyByLevelUser(level, user)
      if len(sc):
        scores[user] = sc
    return scores
   
class ClassificationFusion(ClassificationMultiD):
  def __init__(self, start, length):
    super(ClassificationFusion, self).__init__(start, length)
    #weights = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    self.weights = [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]

  def classifyByLevelMultiRef(self, ref):
    scores = {}
    for ft in mldata.enfeatures:
      scores[ft] = self.classifyByLevelFeatureRef(self.level, ft)

    finalscores = {}
    for user in self.userlvl:
      finalscores[user] = 0
      for ft in mldata.enfeatures:
        finalscores[user] += scores[ft][user] * self.weights[ft]
    return finalscores

