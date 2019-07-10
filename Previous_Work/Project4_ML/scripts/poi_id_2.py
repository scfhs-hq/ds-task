#!/usr/bin/python


import sys
import pickle
sys.path.append("/home/yaser/Udacity/P5/P5_YasserAlnakhli/tools")
import pandas as pd
import numpy as np
from numpy import log


import sys
import pickle
import matplotlib.pyplot as plt
from Select_BFeatures import get_k_best, create_add_features
from tester import test_classifier, dump_classifier_and_data
from feature_format import featureFormat, targetFeatureSplit
from sklearn.feature_selection import SelectFromModel, SelectKBest, f_classif
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn import cross_validation
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV
from sklearn import datasets, metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import LogisticRegression



################## Task 1: features  selection ########################3


###  A: features:

main_feature = ['poi']


features_financial =[
                    'salary', 
                    'deferral_payments', 
                    'total_payments', 
                    'loan_advances', 
                    'bonus', 
                    'restricted_stock_deferred', 
                    'deferred_income', 
                    'total_stock_value', 
                    'expenses', 
                    'exercised_stock_options', 
                    'other', 
                    'long_term_incentive', 
                    'restricted_stock', 
                    'director_fees'
                    ]

features_email = [
                "from_messages",
                "from_poi_to_this_person",
                "from_this_person_to_poi",
                "shared_receipt_with_poi",
                "to_messages"
                ]



### B: load the dictionary containing the dataset
data_dict = pickle.load(open("/home/yaser/Udacity/P5/P5_YasserAlnakhli/scripts/final_project_dataset.pkl", "r") )

##############################################
###Required from the reviwer 1. ############
##############################################
# I used a method in the tools/ directory. from Select_BFeatures import get_k_best, create_add_features
# create_add_features will creat the following:


# To add new feature, Log transformation has been applied to some features

features_new = ["total_payments_log",
                "salary_log",
                "bonus_log",
                "total_stock_value_log",
                "exercised_stock_options_log"]



features_list = main_feature+ features_financial + features_email +features_new
#print(features_list)

data_dict = create_add_features(data_dict, features_list, financial_log=True)


### Store to my_dataset for easy export below.
my_dataset = data_dict



### My main features list will be :
#features_list = main_feature+ financial_features + features_email # + new_features



### C: Explore my Dataset 
print('Dataset Exploration:')
my_dataset.keys()

print('Data points: %d' % len(my_dataset.keys()))

# POI and not POI
num_poi = 0
for name in my_dataset.keys():
    if my_dataset[name]['poi'] == True:
        num_poi += 1
print('# of POI: %d' % num_poi)
print('# of not POI: %d' % (len(my_dataset.keys()) - num_poi))



################## Task 2: Outliers and NaNs ########################3

### A: Outliers, there are more details about this in the report
#outliers = ['TOTAL','LOCKHART EUGENE E' ,'THE TRAVEL AGENCY IN THE PARK']
#
my_dataset.pop('TOTAL', 0)

my_dataset.pop('LOCKHART EUGENE E', 0)

my_dataset.pop('THE TRAVEL AGENCY IN THE PARK', 0)


### B: NaNs replacemnt:
my_dataset.pop('NaN', 0)
#features_list.pop('NaN', 0)




################## Task 3: Define the Best Features ########################3
'''modified from the original post on :
# https://discussions.udacity.com/t/project-identify-fraud-from-enron-email/259175'''


### A: Best Features

num_features= 16

def get_k_best(data_dict, features_list, k):
    """ using SelectKBest feature selection
        returns dict where keys=features, values=scores
    """
    data = featureFormat(my_dataset, features_list)
    labels, features = targetFeatureSplit(data)

    k_best = SelectKBest(k=k)
    k_best.fit(features, labels)
    scores = k_best.scores_
    unsorted_pairs = zip(features_list[1:], scores)
    sorted_pairs = list(reversed(sorted(unsorted_pairs, key=lambda x: x[1])))
    k_best_features = dict(sorted_pairs[:k])
    print "{0} best features: {1}\n".format(k, k_best_features.keys())
    return k_best_features

best_features = get_k_best(my_dataset, features_list, num_features)
my_best_feature_list = main_feature + best_features.keys()
print (my_best_feature_list)


### B: Using featureFormate tool to extract features and labels from dataset for local testing
#from feature_format import featureFormat, targetFeatureSplit

data = featureFormat(my_dataset, my_best_feature_list, sort_keys = True)
labels, features = targetFeatureSplit(data)


### C: Using cross validation to split train 
#from sklearn.cross_validation import train_test_split


seed = 7
test_size = 0.33
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=test_size, random_state=seed)



################## Task 4: Try a varity of classifiers and Tuning  ########################3

# Using  xgboost import XGBClassifier
from numpy import loadtxt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

"""
clf_XGB= XGBClassifier()

clf_XGB.fit(features_train, labels_train)
score = metrics.accuracy_score(labels_test, clf_XGB.predict(features_test))
print("Accuracy  with tunned MLPClassifier: %f" % score)
recall= recall_score(labels_test, clf_XGB.predict(features_test))
print("recall with tunned MLPClassifier: %f" %recall)
precision = precision_score(labels_test, clf_XGB.predict(features_test))
print("precision with tunned MLPClassifier: %f" %precision)

F1 = 2 * (precision * recall) / (precision + recall)
print("the F1 score with tunned MLPClassifier is: %f" %F1)

print("=========================================")
print("=========================================")
print("=========================================")

test_classifier(clf_XGB, my_dataset, features_list)


print("=========================================")
print("=========================================")
print("=========================================")
"""

### A: LogisticRegression 
#from sklearn.linear_model import LogisticRegression

clf_LR = LogisticRegression()
clf_LR.fit(features_train, labels_train)
score = metrics.accuracy_score(labels_test, clf_LR.predict(features_test))
print("Accuracy with LR: %f" % score)
recall= recall_score(labels_test, clf_LR.predict(features_test))
print("recall with LR: %f" %recall)
precision = precision_score(labels_test, clf_LR.predict(features_test))
print("precision with LR: %f" %precision)

F1 = 2 * (precision * recall) / (precision + recall)
print("the F1 score with LR is: %f" %F1)

print("=========================================")

### B: Using naive_bayes
#from sklearn.naive_bayes import GaussianNB
from sklearn.calibration import CalibratedClassifierCV


##########################################

clf_NB2 = GaussianNB()
params_NBB1 = {'priors' : [None, [0.1,0.9],[0.2, 0.8]] }

clf_NB = GridSearchCV(clf_NB2, params_NBB1)



#clf_NB= GaussianNB(priors=[0.1, 0.9])
clf_NB.fit(features_train, labels_train)
score = metrics.accuracy_score(labels_test, clf_NB.predict(features_test))
print("Accuracy with NB: %f" % score)
recall= recall_score(labels_test, clf_NB.predict(features_test))
print("recall with NB: %f" %recall)
precision = precision_score(labels_test, clf_NB.predict(features_test))
print("precision with NB: %f" %precision)

F1 = 2 * (precision * recall) / (precision + recall)
print("the F1 score with NB is: %f" %F1)
print("=============  look above  ============================")
## ############################
#Scaling NB

clf_NB2 = GaussianNB()

#Scaling
scaler = preprocessing.MinMaxScaler()
Scale_features_train = scaler.fit_transform(features_train)
Scale_features_test = scaler.fit_transform(features_test)

clf_NB2.fit(Scale_features_train, labels_train)
score = metrics.accuracy_score(labels_test, clf_NB2.predict(Scale_features_test))
print("Accuracy of scalled features NB: %f" % score)
recall= recall_score(labels_test, clf_NB2.predict(Scale_features_test))
print("recall of scalled features NB: %f" %recall)
precision = precision_score(labels_test, clf_NB2.predict(Scale_features_test))
print("precision of scalled features NB: %f" %precision)

F1 = 2 * (precision * recall) / (precision + recall)
print("the F1 score of scalled features NB: %f" %F1)  


print("=================BernoulliNB========================")
# NB 
from sklearn.naive_bayes import BernoulliNB


clf_NNN= BernoulliNB()
params_NNN = {'alpha': [0.05 , 0.08 , 0.09 , 0.1 , 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            'binarize': [0.0, 0.1,0.5,0.05, 0.01,0.001,],
            'fit_prior' : [True, False]}


clf_NB3 = GridSearchCV(clf_NNN, params_NNN)

#Scalin
scaler = preprocessing.MinMaxScaler()
Scale_features_train = scaler.fit_transform(features_train)
Scale_features_test = scaler.fit_transform(features_test)

clf_NB3.fit(Scale_features_train, labels_train)
score = metrics.accuracy_score(labels_test, clf_NB3.predict(Scale_features_test))
print("Accuracy of scalled features BernoulliNB: %f" % score)
recall= recall_score(labels_test, clf_NB3.predict(Scale_features_test))
print("recall of scalled features BernoulliNB: %f" %recall)
precision = precision_score(labels_test, clf_NB3.predict(Scale_features_test))
print("precision of scalled features BernoulliNB: %f" %precision)

F1 = 2 * (precision * recall) / (precision + recall)
print("the F1 score of scalled featuresBernoulliNB: %f" %F1) 

print("=========================================")


### C-1: Using Decision Tree
#from sklearn.tree import DecisionTreeClassifier

clf_DT = DecisionTreeClassifier()

clf_DT.fit(features_train, labels_train)
score = metrics.accuracy_score(labels_test, clf_DT.predict(features_test))
print("Accuracy with DTree: %f" % score)
recall= recall_score(labels_test, clf_DT.predict(features_test))
print("recall with DTree: %f" %recall)
precision = precision_score(labels_test, clf_DT.predict(features_test))
print("precision with DTree: %f" %precision)

F1 = 2 * (precision * recall) / (precision + recall)
print("the F1 score with DTree is: %f" %F1)   
print("=========================================")

### C-2: tunning the DT classifier
''' THe prevoius use of DT classifaier need to be tuned 
GridSearchCV and scaling the features will be used to impver the performance.
I used scalling and GridSearchCV separately, but i did not get a better scores.

I used them together, and the perforamce has improved.'''


clf_tree = DecisionTreeClassifier()
params_tree = { "min_samples_split":[2, 5, 10],
                "criterion": ('gini', 'entropy'),
                "max_features": ["sqrt", "log2"],
                "max_depth":[2, 3]}
classifier4 = GridSearchCV(clf_tree, params_tree)
#scalling the features
scaler = preprocessing.MinMaxScaler()
Scale_features_train = scaler.fit_transform(features_train)
Scale_features_test = scaler.fit_transform(features_test)
classifier4.fit(Scale_features_train, labels_train)
score = metrics.accuracy_score(labels_test, classifier4.predict(Scale_features_test))
print("Accuracy of scalled featuresand tunned with DTree: %f" % score)
recall= recall_score(labels_test, classifier4.predict(Scale_features_test))
print("recall of scalled features and tunned with DTree: %f" %recall)
precision = precision_score(labels_test, classifier4.predict(Scale_features_test))
print("precision of scalled features and tunned with DTree: %f" %precision)

F1 = 2 * (precision * recall) / (precision + recall)
print("the F1 score of scalled features and tunned with DTree is: %f" %F1)  



print("=========================================")

### D-1: Using NN
from sklearn.neural_network import MLPClassifier


clf_NN = MLPClassifier()
clf_NN.fit(features_train, labels_train)
score = metrics.accuracy_score(labels_test, clf_NN.predict(features_test))
print("Accuracy with MLPClassifier: %f" % score)
recall= recall_score(labels_test, clf_NN.predict(features_test))
print("recall with MLPClassifier: %f" %recall)
precision = precision_score(labels_test, clf_NN.predict(features_test))
print("precision with MLPClassifier: %f" %precision)


F1 = 2 * (precision * recall) / (precision + recall)
print("the F1 score with MLPClassifier is: %f" %F1)
print("=========================================")

### D-1: Using NN with scalled
from sklearn.neural_network import MLPClassifier

classifier5 = MLPClassifier()
scaler = preprocessing.MinMaxScaler()
Scale_features_train = scaler.fit_transform(features_train)
Scale_features_test = scaler.fit_transform(features_test)

classifier5.fit(Scale_features_train, labels_train)
score = metrics.accuracy_score(labels_test, classifier5.predict(Scale_features_test))
print("Accuracy with MLPClassifier scaled features: %f" % score)
recall= recall_score(labels_test, classifier5.predict(Scale_features_test))
print("recall with MLPClassifier scaled features: %f" %recall)
precision = precision_score(labels_test, classifier5.predict(Scale_features_test))
print("precision with MLPClassifier scaled features: %f" %precision)

F1 = 2 * (precision * recall) / (precision + recall)
print("the F1 score with MLPClassifier scaled features is %f" %F1) 

print("=========================================")



### D-2: tuning NN Classifier 

clf_NN= MLPClassifier()
params_NN = {
            'hidden_layer_sizes': [10, 20],
            'activation': ['logistic', 'relu'],
            'max_iter': [150, 200]}

classifier1 = GridSearchCV(clf_NN, params_NN)
classifier1.fit(features_train, labels_train)
score = metrics.accuracy_score(labels_test, classifier1.predict(features_test))
print("Accuracy  with tunned MLPClassifier: %f" % score)
recall= recall_score(labels_test, classifier1.predict(features_test))
print("recall with tunned MLPClassifier: %f" %recall)
precision = precision_score(labels_test, classifier1.predict(features_test))
print("precision with tunned MLPClassifier: %f" %precision)

F1 = 2 * (precision * recall) / (precision + recall)
print("the F1 score with tunned MLPClassifier is: %f" %F1)

print("=========================================")




################## Task 5: Select the Best classifiers ########################3

#test_classifier(clf_NB, my_dataset, features_list)
### Select NB as final algorithm

# from the scores for all the above classifiers, NB got the best scores amoge others. 
print("=================   LR   ========================")

test_classifier(clf_LR, my_dataset, features_list)

print("================== NB      =======================")

test_classifier(clf_NB, my_dataset, features_list)

print("================ NB Scaled Features================")

test_classifier(clf_NB2, my_dataset, features_list)



####         The best ALg I got  ######################################
#######################################################################
# Please comment this for a faster run


#THis gives the best result.. but it take loooge time to run.. about 20 min
print("===============  BernoulliNB  ================")
test_classifier(clf_NB3, my_dataset, features_list)

                                 
########################################################################


print("================   DTree    ========================")

test_classifier(clf_DT, my_dataset, features_list)



print("====================  NN ============================")

test_classifier(clf_NN, my_dataset, features_list)


print("====================  NN Scalled F =================")

test_classifier(classifier5, my_dataset, features_list) 






# dump the best classifier, dataset and features_list so
# anyone can run/check your results

dump_classifier_and_data(clf_NB, my_dataset, my_best_feature_list)