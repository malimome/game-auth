import data as mldata
import pdb

class ClassificationBase(object):
  def __init__(self, start, length):
    self.start = start
    self.length = length
    self.userlvl = dict()
    #self.ud,self.mincLF = self.readProfiles()  #ud is the user data per level feature
    self.profiles = {}
    self.attempt = {}
    self.mindtPr = {}
    #self.ulf = dict() #the training data
    #self.ulftest = dict()   # the test data
    self.level = -1

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

  def readAttempt(self, level, user):
    users = mldata.getUsers(is_profile = False)
    if user not in users:
      return False, False
    dtuser = mldata.UserData(user, is_profile = False)
    udcount = dtuser.getUserFeatureLevels()
    return dtuser.ftlevels,udcount

  def readPAdata(self, level, user=''):
    if not self.profiles:
      self.profiles,self.mindtPr = self.readProfiles()
    #if self.profiles
    if user=='':
      return True
    self.attempt, tmp = self.readAttempt(level, user)
    #if self.attempt == False:
    #  return False

  def classifyByFeature(self, feature):
    levelscores = {}
    for level in self.profiles.ftlevels:
      levelscores[level] = self.classifyByLevelFeature(level, feature)

  def classifyUsers(self):
    allscores = {}
    for level in mldata.levelenum:
      allscores[level] = self.classifyByLevel(level)
    return allscores

class ClassificationOneD(ClassificationBase):
  def __init__(self, start, length):
    super(ClassificationOneD, self).__init__(start, length)

  def classifyByLevelFeature(self, level, feature):
    if not self.readPAdata(level, feature):
      return {}
    refscores = {}
    for ref in self.userlvl[level]:
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
    if not self.readPAdata(level):
      return {}
    refscores = {}
    if user != '':
      return self.classifyByLevelMultiRef(user)

    for ref in self.userlvl[level]:
      refscores[ref] = self.classifyByLevelMultiRef(ref)
    return refscores  

  def classifyByLevelUser(self, level, user):
    pdb.set_trace()
    self.readPAdata(level, user)
    self.level = level
    #  return {}
    scores = self.classifyByLevelFeature(level, user)
    return scores
 
  def classifyByLevel(self, level):
    if not self.readPAdata(level):
      return {}
    self.level = level
    scores = self.classifyByLevelFeature(level)
    return scores
   
class ClassificationFusion(ClassificationMultiD):
  def __init__(self, start, length):
    super(ClassificationFusion, self).__init__(start, length)
    #weights = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    self.weights = [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]
    #weights = [0.65, 0.6, 0.55, 0.5, 0.5, 0.3, 0.3, 0.2]

  def classifyByLevelMultiRef(self, ref):
    scores = {}
    for ft in mldata.enfeatures:
      scores[ft] = self.classifyByLevelFeatureRef(self.level, ft)

    finalscores = {}
    for user in self.userlvl[self.level]:
      finalscores[user] = 0
      for ft in mldata.enfeatures:
        finalscores[user] += scores[ft][user] * self.weights[ft]
    return finalscores

