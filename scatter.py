import data as mldata
import pprint
import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import colorsys
import pdb

class Scatter_Multi():
  def __init__(self, level):
    self.level = level

  def getUsersData(self):
    users = mldata.getUsers()
    ud = {}
    udcount = {}
    mincountperL = {}
    for user in users:
      dtuser = mldata.UserData(user)
      udcnt = dtuser.getUserFeatureLevels()
      if udcnt[self.level] <= 100:
        continue
      udcount[user] = udcnt[self.level]
      ud[user] = dtuser.ftlevels[self.level] 
      #data from all levels and features for one user
    return ud,udcount

  def get_colors(self, N):
    HSV_tuples = [(x*1.0/N, 0.7, 0.7) for x in range(N)]
    random.shuffle(HSV_tuples)
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    return RGB_tuples

  def get_style(self, N):
    style = "-;--;-.;:".split(';')
    marking = "1.D,ov3^s<4>p*h|H+x2+d"
    ret = []
    for m in marking:
      for s in style:
        ret.append(m+s)
    if len(ret) > N:
      print "problem"
    return ret
 
  def get_marker(self, N):
    marking = "x_o^v*sph+h8,4>3.2<1|"
    return marking.split('')

  def display_plot(self):
    ud,udcount = self.getUsersData()
    plt.figure()
    N = 5
    RGB_tuples = self.get_colors(N)
    j = 1
    for ft in mldata.enfeatures:
      plt.subplot(2,2,j)
      j+=1
      i = 0
      for user in ud.keys()[:N]:
        plt.plot(sorted(ud[user][ft]), color = RGB_tuples[i])
        i += 1
        plt.title(mldata.features[ft]['name'])
    plt.show()
    
  def display_scatter(self):
    ud,udcount = self.getUsersData()
    marking = "x_o^v*sph+h8,4>3.2<1|"
    N = 6
    i = 0
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #ax1 = fig.add_subplot(122, projection='3d')
    RGB_tuples = self.get_colors(N)
#    ax.set_title('')
    for user in ud.keys()[:N]:
      crd = range(3)
      for ind,ft in enumerate(ud[user]):
        crd[ind] = ud[user][ft]
        if ind >= 2: break
      ax.scatter(crd[0],crd[1],crd[2],color=RGB_tuples[i],marker=marking[i%len(marking)])
      #ax1.scatter(crd[3],crd[4],crd[5],color=RGB_tuples[i], marker=marking[i%len(marking)])
      i += 1
    plt.legend(loc='lower left',ncol=3,fontsize=8)
    def setxyz(ax, a=0,b=0):
      ax.set_xlabel('x', fontsize=16)
      ax.set_ylabel('y', fontsize=16)
      ax.set_zlabel('z', fontsize=16)
      #ax.set_xticks([-2,-1,0,1,2,3,4,5,6,7,8])
      #ax.set_yticks([0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
      #ax.set_xlim(0,4)
      #ax.set_ylim(0.4, 0.6)
      ax.view_init(a, b)
    #setxyz(ax,45,45)
    setxyz(ax,90,-90)
    plt.show()

    
      

