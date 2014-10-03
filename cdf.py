from mlerror import ErrEmptyData
from classifier import ClassificationOneD, ClassificationFusion
#rom scipy import stats
import scipy.special as special
import numpy as np
import pdb
import data
DEBUGL = data.DEBUGL

ksprob = special.kolmogorov
class ClassificationCDF(ClassificationOneD):
  def __init__(self, start, length):
    super(ClassificationCDF, self).__init__(start, length)

  def classifyByLevelFeatureRef(self, level, feature):
    test = self.attempt[feature]
    scores = dict()
    for user in self.userlvl:
      data = self.profiles[user][feature]
      scores[user] = self.classifySimilarity(data, test, feature)
    return scores

  def classifySimilarity(self, data, test, feature):
    if not data or not test:
      raise ErrEmptyData
    d,pval = self.ks_2samp(data, test)
    if DEBUGL >= 2:
      print("Length of profile: %d, Length of login %d"%(len(data), len(test)))
      print("Distance: %f, Prob: %f"%(d,pval))
    return d

  def ks_2samp(self, data1, data2):
    data1, data2 = map(np.asarray, (data1, data2))
    n1 = data1.shape[0]
    n2 = data2.shape[0]
    n1 = len(data1)
    n2 = len(data2)
    data1 = np.sort(data1)
    data2 = np.sort(data2)
    data_all = np.concatenate([data1,data2])
    cdf1 = np.searchsorted(data1,data_all,side='right')/(1.0*n1)
    cdf2 = (np.searchsorted(data2,data_all,side='right'))/(1.0*n2)
    d = np.max(np.absolute(cdf1-cdf2))
    #Note: d absolute not signed distance
    en = np.sqrt(n1*n2/float(n1+n2))
    try:
      prob = ksprob((en+0.12+0.11/en)*d)
    except:
      prob = 1.0
    return d, prob

""" Fusion class """    
class ClassificationCDF_Fusion(ClassificationFusion, ClassificationCDF):
  pass
