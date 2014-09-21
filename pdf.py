from classifier import ClassificationOneD, ClassificationMultiD, ClassificationFusion
import data as mldata
#import pdb

class ClassificationPDF(ClassificationOneD):
  def __init__(self, start, length):
    super(ClassificationPDF, self).__init__(start, length)

  def classifyByLevelFeatureRef(self, level, feature):
    ft = feature
    test = self.attempt[feature]
    maxv = mldata.features[ft]['end']
    minv = mldata.features[ft]['start']
    testhist = self.getHistogram(test, maxv, minv, mldata.features[ft]['step'])
    scores = dict()
    for user in self.userlvl:
      data = self.profiles[user][feature]
      datahist = self.getHistogram(data, maxv, minv, mldata.features[ft]['step'])
      scores[user] = self.getDistance(testhist, datahist)
    return scores

  def getHistogram(self, data, maxv, minv, step):
    hist = {}
    for row in data:
      if row > maxv:
        continue
      binind = int(float(row - minv)/step)
      if binind not in hist:
        hist[binind] = 1
      else:
        hist[binind] += 1
    return hist

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

class ClassificationPDF_Fusion(ClassificationFusion, ClassificationPDF):
  pass

class ClassificationPDF_Multi(ClassificationMultiD, ClassificationPDF):
  def __init__(self, start, length):
    super(ClassificationPDF_Multi, self).__init__(start, length)
    self.maxasbase = 0

  def getHistogram(self, data):
    rowft = 0 
    space = {}
    for ft in data:
      rownum = len(data[ft])
      break
    for rowind in range(0, rownum):
      index = 0
      for ft in mldata.enfeatures:
        rowft = int((data[ft][rowind] - mldata.features[ft]['start'])/mldata.features[ft]['step'])
        if rowft < 0:
          rowft = 0
        index += rowft * pow(self.maxasbase, ft)  #find the unique index 
      if index not in space:
        space[index] = 1
      else:
        space[index] += 1 
    return space

  def classifyByLevelMultiRef(self, ref):
    ftnum = []
    for ft in mldata.enfeatures:
      ftnum.append(float(mldata.features[ft]['end'] - mldata.features[ft]['start'])/mldata.features[ft]['step'])
    self.maxasbase = max(ftnum) + 1
    testhist = self.getHistogram(self.attempt)
    scores = dict()
    for user in self.userlvl:
      datahist = self.getHistogram(self.profiles[user])
      scores[user] = self.getDistance(testhist, datahist)
    return scores

