from sklearn.datasets import load_iris
from sklearn.externals.six import StringIO
from sklearn.cross_validation import train_test_split
from sklearn import tree
import numpy as np
import pydot
from IPython.display import Image
import os

iris  = load_iris()
train_in, test_in, train_out, test_out = train_test_split(iris.data, iris.target,
                                                          test_size=0.2,
                                                          random_state=42)
clf = tree.DecisionTreeClassifier()
class_model = clf.fit(train_in, train_out)
class_results = class_model.predict(test_in)

print '='*20 +' Classifier '+'='*20
print 'Does the model fit perfectly? ', np.all(class_results == test_out)
print 'Model Score: ', class_model.score(test_in,test_out)*100,'%'
print '-'*50

clf = tree.DecisionTreeRegressor()
reg_model = clf.fit(train_in,train_out)
reg_results = reg_model.predict(test_in)

print '='*20 +' Regressor '+'='*20
print 'Does the model fit perfectly? ', np.all(reg_results == test_out)
print 'Model Score: ', reg_model.score(test_in,test_out)*100,'%'
print '-'*50

t = reg_model.tree_
print 'Features'
print t.feature
