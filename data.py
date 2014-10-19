from os import listdir, rename, remove
from os.path import isfile, join, isdir
import time
import pdb

#0 id, 1 rounds, 2 tot_score, 3 time, 4 ballX, 5 ballY, 6 target.X, 7 target.Y, 
#8 shoottime, 9 level, 10 Angle, 11 Velocity, 12 waittime, 13 initMouseX, 14 initMouseY,
#15 refcolor, 16 hitcolor, 17 hit?, 18 score, 19 Ydiff, 12 ip
features = {
            0: {'start': 0, 'end': 16, 'step': 0.2, 
              'func': lambda x: float(x[8]), 'enabled': 1, 'name': 'Shoot time', 
              'sts': 0.1, 'ste': 2.0, 'stt': 0.1, 'meshd': 0.1},
            1: {'start': 0, 'end': 10, 'step': 0.1, 
              'func': lambda x: float(x[12]), 'enabled': 1, 'name': 'Reaction time',
              'sts': 0.05, 'ste': 0.5, 'stt': 0.05, 'meshd': 0.1},
            2: {'start': -220, 'end': 220, 'step': 10, 
              'func': lambda x: float(x[7])-float(x[5]), 'enabled': 1, 'name':'Accuracy',
              'sts': 1, 'ste': 30, 'stt': 1, 'meshd': 5},
            3: {'start': 10, 'end': 150, 'step': 0.1, 
              'func': lambda x: float(x[13]) - 88.5, 'enabled': 1, 'name': 'initMouseX',
              'sts': 0.05, 'ste': 0.5, 'stt': 0.05, 'meshd':0.1},
            4: {'start': 220, 'end': 300, 'step': 0.1, 
              'func': lambda x: float(x[14]) - 268.0, 'enabled': 1, 'name': 'initMouseY',
              'sts': 0.05, 'ste': 0.5, 'stt': 0.05, 'meshd':0.1},
            5: {'start': 0, 'end': 370, 'step': 0.5, 
              'func': lambda x: float(x[10]), 'enabled': 1, 'name': 'Angle',
              'sts': 0.05, 'ste': 0.5, 'stt': 0.05, 'meshd':0.1},
            6: {'start': 1, 'end': 8, 'step': 0.05, 
              'func': lambda x: float(x[11]), 'enabled': 1, 'name': 'Velocity',
              'sts': 0.05, 'ste': 0.5, 'stt': 0.05, 'meshd': 0.01},
            7: {'start': 0, 'end': 16, 'step': 1, 
              'func': lambda x: float(x[-1]), 'enabled': 1, 'name': 'Misses',
              'sts': 0.05, 'ste': 0.5, 'stt': 1, 'meshd': 1},
       }

#enfeatures = [d for d in features if features[d]['enabled']==1] 
enfeatures = [0,1,2,3,4,5,6,7]
def set_enfeatures(fts):
  global enfeatures
  enfeatures = fts
LevelsNoSuffData = [] #[2,3,5,8]
levelenum = [x for x in range(0,9) if x not in LevelsNoSuffData]
filterow  = lambda x: (int(x[17].strip()) == 0) # and abs(float(x[7])-float(x[5])) <= 2000)
getlevel = lambda x: x[9]
dtmaxlen = [[120], [120], [120],[120],[120],[120],[120],[120]]
DEBUGL = 1 #0, 1, 2
dtpathp = "profiles/"
dtpathl = "login/"

def getUsers(is_profile = True):
  global dtpathp, dtpathl
  if is_profile:
    dtpath = dtpathp
  else:
    dtpath = dtpathl
  blacklist = []#"FK__123.csv", "MMS__1362.csv", "AmirT__123.csv", "AH__1234.csv"]#, "User1__123.csv"]
  if not isdir(dtpath):
    dtpath = "./"
  users = [ f for f in listdir(dtpath) if (f.endswith(".csv") and isfile(join(dtpath,f)) and f not in blacklist)]
  #users = users[:4]
  if len(users)==0:
    print("No user files, please put the files in current directory.")
    exit(0)
  #users = ["oldmohsen.csv1", "oldnarges.csv1", "oldhossein.csv1"]
  #users = users[0:10] #TODO
  if DEBUGL >= 2 and is_profile:
    print("Users in classification \t %s"%str(users))
    ftstr = "Features: \t\t\t "
    for ft in enfeatures:
      ftstr += features[ft]['name'] + " "
    print(ftstr)
  return users


class UserData:
#data for one user
  def __init__(self, user, level, is_profile = True):
    global dtpathp
    global dtpathl
    if is_profile:
      self.dtpath = dtpathp
    else:
      self.dtpath = dtpathl
    self.level = level
    self.rawdata = [] #all data for one user all rows
    self.rawcount = 0
    self.rawdtlevels = {} #data for user per level
    self.ftlevels = {}    #user data per level feature
    self.filtered_sof = {}
    self.user = user

  def getUserRawData(self, nofilter):
    """ Get all data in the file for the user class is initialized with"""
    if self.rawdata:
      return
    dtfile = self.dtpath + self.user
    if self.rawcount != 0:
      return True
    self.rawcount = -1
    for ft in enfeatures:
      self.ftlevels[ft] = []
    datacount = 0
    for line in open(dtfile):
      if self.rawcount == -1:
        self.rawcount += 1
        continue
      self.rawcount += 1
      line = line.strip()
      row= [x.strip() for x in line.split(",")]
      self.filtered_sof = 0
      #self.rawdtlevels = []
      #if self.dtpath == "login/":
        #pdb.set_trace()
      try:
        if self.filterData(row):
          row.append(self.filtered_sof)
          self.filtered_sof = 0
        #  self.rawdtlevels.append(row) # prob here
          for ft in enfeatures:
            self.ftlevels[ft].append(features[ft]['func'](row))
      except:
        print "problem in row " + line + '\n';
        continue
    #pdb.set_trace()
    datacount = len(self.ftlevels[0])
    return datacount

  def filterData(self, row):
    lev = int(getlevel(row))
    #if lev in LevelsNoSuffData:
    #  return False
    if lev != self.level:
      return False
    if filterow(row): #TODO can be eliminated or used as an extra feature
      self.filtered_sof += 1
      return False
    return True

  def getUserFeatureLevels(self, nofilter = False):
    return self.getUserRawData(nofilter)

  def moveData(self, archive = False, mvdest = False):
    global dtpathp, dtpathl
    pfile = dtpathp + self.user
    lfile = dtpathl + self.user
    # rename the file but not add to profile
    if archive:
      fpath = lfile
      # move the file to a new dir
      if mvdest:
        fpath = dtpathl + 'failed/' + self.user
      tmp = str(int(time.time()))
      try:
        rename(lfile, fpath + tmp)
      except Exception as e:
        return str(e)
      return ''
    cnt = -1
    with open(pfile, "a") as pf:
      lf = open(lfile)
      for line in lf:
        if cnt == -1:
          cnt += 1
          continue
        pf.write(line)
    lf.close()
    remove(lfile)
    return ''




