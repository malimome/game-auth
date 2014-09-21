import numpy as np
import pylab as pl
from matplotlib.colors import ListedColormap
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA
from classifier import ClassificationMultiD
import data as mldata
import pdb

class ClassificationML_Multi(ClassificationMultiD):
  def __init__(self, start, length, method):
    super(ClassificationML_Multi, self).__init__(start, length)
    self.method = method

  def runClassifiers(self, X, y, X_train, y_train, X_test, y_test):
    #d1,d2 = mldata.enfeatures[0], mldata.enfeatures[1]
    #h1 = mldata.features[d1]['meshd']  # step size in the mesh
    #h2 = mldata.features[d2]['meshd']
    h1 = 1
    h2 = 1

    #names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Decision Tree",
    #         "Random Forest", "AdaBoost", "Naive Bayes", "LDA", "QDA"]
    classifiers = {
        "nearest_neighbors": KNeighborsClassifier(5),
        "linear_svm": SVC(kernel="linear", C=0.025),
        "poly_svm": SVC(kernel="poly", degree=2),#, gamma=1, C=1),
        "decision_tree": DecisionTreeClassifier(max_depth=None),
        "random_forest": RandomForestClassifier(max_depth=None, n_estimators=5, max_features=5, criterion="gini"),
        "adaboost": AdaBoostClassifier(),
        "naive_bayes": GaussianNB(),
        "lda": LDA(),
        "qda": QDA()}

    """
    figure = pl.figure(figsize=(27, 9))
    i = 1
    #pdb.set_trace()
    x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
    #print x_min, x_max
    #print y_min, y_max
    #x_min,x_max = 0,10
    #y_min,y_max = -110,110
    #pdb.set_trace()
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h1),
                         np.arange(y_min, y_max, h2))

    datasets = [1]
    # just plot the dataset first
    #cm = pl.cm.RdBu
    cm = pl.cm.Paired
    cm_bright = ListedColormap(['#FF0000', '#00FF00', '#0000FF', 
        "#FFFF00", "#FF00FF"])#, "#00FFFF", "#000000", 
    #    "#800000", "#008000", "#000080", "#808000", "#800080", "#008080", "#808080"
    #])
    ax = pl.subplot(len(datasets), 1 + 1, i)
    # Plot the training points
    ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright)
    # and testing points
    ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, alpha=0.6)
    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())
    ax.set_xticks(())
    ax.set_yticks(())
    i += 1
    #pl.show()
"""
    datasets = [1]
    # iterate over classifiers
    #for name, clf in zip(names, classifiers):
    if self.method != "":
      name = self.method
      clf = classifiers[name]
      #ax = pl.subplot(len(datasets), 1 + 1, i)
      clf.fit(X_train, y_train)
      yp = clf.predict(X_test)
      l = abs(self.length)
      y_class = [yp[:l],yp[l:2*l],yp[2*l:3*l],yp[3*l:4*l],yp[4*l:]]
      scr = 0
      #pdb.set_trace()
      for ind,lst in enumerate(y_class):
        bc = np.bincount(lst)
        maxval = max(bc)
        items = []
        for i,val in enumerate(bc):
          if bc[i] == maxval:
            items.append(i)
        #print ind, items
        if ind in items:
          scr += 1.0/(5*len(items))
      score = clf.score(X_test, y_test)
      print "Class detection success \t %%%d \nData classificaion success \t %%%d"%(scr*100,score*100)
      return
      
      # Plot the decision boundary. For that, we will assign a color to each
      # point in the mesh [x_min, m_max]x[y_min, y_max].
      if hasattr(clf, "decision_function"):
        Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
      else:
        Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]

      """
      # Put the result into a color plot
      Z = Z.reshape(xx.shape)
      ax.contourf(xx, yy, Z, cmap=cm, alpha=.8)

      # Plot also the training points
      ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright)
      # and testing points
      ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright,
                   alpha=0.6)

      ax.set_xlim(xx.min(), xx.max())
      ax.set_ylim(yy.min(), yy.max())
      ax.set_xticks(())
      ax.set_yticks(())
      ax.set_title(name)
      ax.text(xx.max() - .3, yy.min() + .3, ('%.2f' % score).lstrip('0'),
                size=15, horizontalalignment='right')
      i += 1

    figure.subplots_adjust(left=.02, right=.98)
    pl.show()
    """

  def classifyByLevelMultiRef(self, ref = ""):
    X = []
    y = []
    X_train = []
    y_train = []
    X_test = []
    y_test = []
    X = []
    y = []
    corresp = {}
    ind = 0
    for user in self.userlvl:
      corresp[user] = ind
      for ft in mldata.enfeatures:
        userlen = len(self.profiles[user][ft])
        userlentest = len(self.attempt[ft])
        break
      for i in range(userlen):
        iuserft = []
        for ft in mldata.enfeatures:
          iuserft.append(self.ulf[user][ft][i])
        X_train.append(iuserft)
        y_train.append(ind)
        X.append(iuserft)
        y.append(ind)
      for i in range(userlentest):
        iuserftest = []
        for ft in mldata.enfeatures:
          iuserftest.append(self.ulftest[user][ft][i])
        X_test.append(iuserftest)
        y_test.append(ind)
        X.append(iuserftest)
        y.append(ind)
      ind += 1

    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_test = np.array(X_test)
    y_test = np.array(y_test)
    X= np.array(X)
    y= np.array(y)
    #del self.ulf
    #del self.ulftest
    #pdb.set_trace()
    #del self.ud
    #gc.collect()
    self.runClassifiers(X, y, X_train, y_train, X_test, y_test)
    return []

  def classifyByLevelFeature(self, level, feature = -1):
    if not self.readPAdata(level, feature):
      return {}
    refscores = self.classifyByLevelMultiRef()
    return refscores  


