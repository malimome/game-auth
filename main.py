import svm
import cdf, pdf
import scatter
import data
import numpy as np
import pdb


uave = {}
umiss = {}

def getStats(result, udftlevel):
  for user in result:
    ftlevel = udftlevel[user]
    ydiffs = np.array(ftlevel[level][2])
    umiss[user] = sum(ftlevel[level][7])
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
def display_vrf(result, ud_ftlevel):
  global uave, umiss
  WARN = '\033[91m'
  END = '\033[0m'
  print("Number of users in experiment: \t%d"%len(result))
  print("------------------------------------")
  print("uind -> udist Y/N #ufacc uave umiss")
  flag = 0
  zeta = 0.65
  getStats(result, ud_ftlevel)
  allusers = sorted(result.iterkeys(), key = lambda user: 4*uave[user] + umiss[user])
  AllY = 0
  um = ""
  usermap = ""
  rs = ""
  resultstr = ""
  for refuser in allusers:
    d = result[refuser]
    ds = sorted(d.itervalues())
    zeta = ds[1]
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

import string
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

def split_args(option, opt, value, parser):
  ret = []
  for f in value.split(','):
    if f.strip() != "":
      ret.append(int(f.strip()))
  setattr(parser.values, option.dest, ret)

names = ["nearest_neighbors", "linear_svm", "poly_svm", "decision_tree",
         "random_forest", "adaboost", "naive_bayes", "lda", "qda"]
allmethods = list(names)
allmethods.extend(["cdf_fusion","pdf_fusion","pdf_multi","cdf","pdf"])
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-m", "--method", dest="method", default="random_forest",
    help="One of %s"%str(allmethods))
parser.add_option("-l", "--level", dest="level", default=3, type=int, help="Level of the game")
parser.add_option("-w", "--width", dest="length", default=-30)
parser.add_option("-b", "--begin", dest="start", default=0)
parser.add_option("-f", "--features", dest="features", 
    default='0,1,2,3,4', action='callback', callback=split_args, type='str',
    help="List of features 0,1,2,3,4")
(options, args) = parser.parse_args()
level = options.level
length = int(options.length)
method = options.method
start = int(options.start)
data.enfeatures = options.features
pdb.set_trace()

print ("__________________________________________________________________________")
if method.strip().isdigit():
  method = allmethods[int(method)]
print("Classification method used: \t %s"%method)
if method == "scatter":
  cls = scatter.Scatter_Multi(level)
  cls.display_scatter()
elif method == "plot":
  cls = scatter.Scatter_Multi(level)
  cls.display_plot()
if method in names:
  cls = svm.ClassificationML_Multi(start, length, method)
  refscores = cls.classifyByLevel(level)
elif method == "cdf_fusion":
  ccdf = cdf.ClassificationCDF_Fusion(start, length)
  refscores = ccdf.classifyByLevel(level)
  #display_result(refscores)
  display_vrf(refscores, ccdf.ud)
elif method == "pdf_fusion":
  ccdf = pdf.ClassificationPDF_Fusion(start, length)
  refscores = ccdf.classifyByLevel(level)
  display_result(refscores)
elif method == "pdf_multi":
  cls = pdf.ClassificationPDF_Multi(start, length)
  refscores = cls.classifyByLevel(level)
  display_result(refscores)
elif method == "cdf":
  ccdf = cdf.ClassificationCDF(start, length)
  refscores = ccdf.classifyByLevel(level)
  for ft in data.features:
    refscores[data.features[ft]['name']] = refscores.pop(ft)
    print("---------feature %s -------------"%data.features[ft]['name'])
    display_result(refscores[data.features[ft]['name']])
elif method == "pdf":
  cb = pdf.ClassificationPDF(start, length)
  refscores = cb.classifyByLevel(level)
  for ft in data.features:
    refscores[data.features[ft]['name']] = refscores.pop(ft)
    print("---------feature %s -------------"%data.features[ft]['name'])
    display_result(refscores[data.features[ft]['name']])
print ("__________________________________________________________________________")


