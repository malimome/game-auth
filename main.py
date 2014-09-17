import svm
import cdf, pdf
import scatter
import data
from display import *
import numpy as np
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
parser.add_option("-m", "--method", dest="method", default="random_forest",
    help="One of %s"%str(allmethods))
parser.add_option("-l", "--level", dest="level", default=3, type=int, help="Level of the game")
parser.add_option("-w", "--width", dest="length", default=-30)
parser.add_option("-b", "--begin", dest="start", default=0)
parser.add_option("-f", "--features", dest="features", 
    default='0,1,2,3,4', action='callback', callback=split_args, type='str',
    help="List of features 0,1,2,3,4")
parser.add_option("-u", "--user", dest="user", default='')
(options, args) = parser.parse_args()
level = options.level
length = int(options.length)
method = options.method
start = int(options.start)
user = options.user
data.enfeatures = options.features
#pdb.set_trace()

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
  display_vrf(refscores, ccdf.ud, level)
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


