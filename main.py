#import svm
import cdf, pdf
import scatter
import data
from display import *
import numpy as np
import analyse
import pdb

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
parser.add_option("-m", "--method", dest="method", default="cdf_fusion",
    help="One of %s"%str(allmethods))
parser.add_option("-l", "--level", dest="level", default=3, type=int, help="Level of the game")
parser.add_option("-w", "--width", dest="length", default=-30)
parser.add_option("-b", "--begin", dest="start", default=0)
parser.add_option("-f", "--features", dest="features", 
    default='0,1,2,3,4,5,6,7', action='callback', callback=split_args, type='str',
    help="List of features 0,1,2,3,4")
parser.add_option("-u", "--user", dest="user", default='')
parser.add_option("-d", "--debug", dest="debug", default=1)
parser.add_option("-o", "--move", dest="move", default=1)
(options, args) = parser.parse_args()
level = options.level
length = int(options.length)
method = options.method
start = int(options.start)
user = options.user
debug = options.debug
data.enfeatures = options.features
data.DEBUGL = debug
# if move==0, then do not add to profile
move = int(options.move)
if move == 1:
  archive = False
  mvdest = False
else:
  archive = True
  mvdest = True
if not debug:
  print ("__________________________________________________________________________")
if method.strip().isdigit():
  method = allmethods[int(method)]
if not debug:
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
  if user != '':
    refscores = ccdf.classifyByLevelUser(level, user)
    if not len(refscores):
      print "0"
      print "0"
      print("Ooops! Not enough data for login. At least 30 rounds of game is needed!")
      exit(0)

    ana = analyse.Analyser() 
    fres,rank = ana.calcPercent(user, refscores)
    usdt = data.UserData(user, level)
    if fres >= 0.90:
      print "1"
      print fres;
      print("Accept! User data matches the profile with %2.1f percent success rate."%(int(fres*1000)/10.0))
      usdt.moveData(archive, mvdest)
    else:
      print "0"
      print fres;
      print("Reject! User data didn't match the profile (%2.1f percent matching rate only)."%(int(fres*1000)/10.0))
      usdt.moveData(archive = True, mvdest = True)
    if debug == 1:
      print("Rank= %d"%rank)
  else:
    refscores = ccdf.classifyByLevel(level)
    newdisplay(refscores, ccdf.profiles)
    #display_result(refscores)
    #display_vrf(refscores, ccdf.profiles, level)
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
    if not debug:
      print("---------feature %s -------------"%data.features[ft]['name'])
    display_result(refscores[data.features[ft]['name']])
elif method == "pdf":
  cb = pdf.ClassificationPDF(start, length)
  refscores = cb.classifyByLevel(level)
  for ft in data.features:
    refscores[data.features[ft]['name']] = refscores.pop(ft)
    if not debug:
      print("---------feature %s -------------"%data.features[ft]['name'])
    display_result(refscores[data.features[ft]['name']])
if not debug:
  print ("__________________________________________________________________________")


