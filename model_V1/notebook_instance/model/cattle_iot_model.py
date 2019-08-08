#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


#loading the data for training and testing
train=pd.read_csv("train.csv")
test=pd.read_csv("test.csv")

target_names = ['STANDING', 'SITTING', 'LAYING', 'WALKING', 'WALKING_DOWNSTAIRS',
       'WALKING_UPSTAIRS']

features = train.iloc[:,0:3]
label = train['Activity']
New_features =features

#using only KNN classifier
# Classifiers = KNeighborsClassifier(n_neighbors=3)

from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
Classifiers = [DecisionTreeClassifier(),
               RandomForestClassifier(n_estimators=200),
               GaussianNB(),
               KNeighborsClassifier(n_neighbors=3),
               GradientBoostingClassifier(n_estimators=200)]


test_features=test.iloc[:,0:3]
# test_features.shape


from sklearn.metrics import accuracy_score
import timeit
Time_2=[]
Model_2=[]
Out_Accuracy_2=[]

for clf in Classifiers:
    start_time = timeit.default_timer()
    fit=clf.fit(New_features,label)
    pred=fit.predict(test_features)
    print(clf.__class__.__name__)
    print(classification_report(test['Activity'],pred,target_names=target_names))
    print(confusion_matrix(test['Activity'], pred))
    print("\n")
    elapsed = timeit.default_timer() - start_time
    Time_2.append(elapsed)
    Model_2.append(clf.__class__.__name__)
    Out_Accuracy_2.append(accuracy_score(test['Activity'],pred))
    print(pred)
# fit=Classifiers.fit(New_features,label)
# pred=fit.predict(test_features)
# print(pred)

# Saving model pickle file to disk

# pickle.dump(fit, open('cattle_iot.pkl','wb'))




