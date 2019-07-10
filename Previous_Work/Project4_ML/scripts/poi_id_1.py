#!/usr/bin/python


import sys
import pickle
sys.path.append("/home/yaser/Udacity/P5/P5_YasserAlnakhli/tools")
from tester import test_classifier, dump_classifier_and_data
from feature_format import featureFormat, targetFeatureSplit
from Select_BFeatures import get_k_best
import pandas as pd
from numpy import log

from sklearn.feature_selection import SelectFromModel, SelectKBest
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


financial_features =[
                    'salary', 
                    'deferral_payments', 
                    'total_payments', 
                    'loan_advances', 'bonus', 
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


##############################################
###Suggestion from the reviwer 1. ############
##############################################
###  Create new feature(s)
new_features = [
                # log will be used for some features
                "log_total_payments",
                "log_bonus",
                "log_salary",
                "log_total_stock_value"]



### My main features list will be :
features_list = main_feature+ financial_features + features_email  + new_features


### B: load the dictionary containing the dataset
data_dict = pickle.load(open("/home/yaser/Udacity/P5/P5_YasserAlnakhli/scripts/final_project_dataset.pkl", "r") )


### Add my new features to the dataset
def add_new_features(data_dict, features_list, log_f= False):
    """
    Given the data dictionary of people with features, adds some features to
    """
    for feature in data_dict:

        # If feature is financial, add another variable with log transformation.
        if log_f:
            for fet in features_list:
                try:
                    data_dict[name]['log_'+fet] = Math.log(data_dict[name][fet] + 1)
                except:
                    data_dict[name]['log_'+fet] = NAN_value


my_dataset = data_dict


##############################################
###Suggestion from the reviwer 1. ############
##############################################
# to use pandas data frame
data_dict_DF= pd.DataFrame.from_dict(data_dict, orient='index')


### Store to my_dataset for easy export below.
my_dataset = data_dict



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
###Suggestion from the reviwer 1. ############
##############################################
### A: Outliers, there are more details about this in the report

#
my_dataset.pop('TOTAL', 0)

my_dataset.pop('LOCKHART EUGENE E', 0)

my_dataset.pop('THE TRAVEL AGENCY IN THE PARK', 0)


### B: NaNs replacemnt:
my_dataset.pop('NaN', 0)
#features_list.pop('NaN', 0)


########################################
#Or by using data frame 
#data_dict_DF = data_dict_DF.drop('TOTAL','LOCKHART EUGENE E' ,'THE TRAVEL AGENCY IN THE PARK' axis=0)
#data_dict_DF = data_dict_DF.replace('NaN', 0)




################## Task 3: Define the Best Features ########################3

### A: Best Features

num_features=12

# I will use get_k_best method which has been moved to a separated file
#look at the tools
best_features = get_k_best(my_dataset, features_list, num_features)
my_best_feature_list = main_feature + best_features.keys()
print (my_best_feature_list)


### B: Using featureFormate tool to extract features and labels from dataset for local testing
#from feature_format import featureFormat, targetFeatureSplit

data = featureFormat(my_dataset, my_best_feature_list, sort_keys = True)
labels, features = targetFeatureSplit(data)


##############################################
###Suggestion from the reviwer 1. ############
##############################################


### C: Using cross validation to split train 
#from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)



################## Task 4: Try a varity of classifiers and Tuning  ########################3


### A: LogisticRegression 
#from sklearn.linear_model import LogisticRegression

clf_LR = LogisticRegression(  C=1000,
                                    penalty='l2',
                                    random_state=42,
                                    tol=10**-10,
                                    class_weight='auto')
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

clf_NB= GaussianNB()
clf_NB.fit(features_train, labels_train)
score = metrics.accuracy_score(labels_test, clf_NB.predict(features_test))
print("Accuracy with NB: %f" % score)
recall= recall_score(labels_test, clf_NB.predict(features_test))
print("recall with NB: %f" %recall)
precision = precision_score(labels_test, clf_NB.predict(features_test))
print("precision with NB: %f" %precision)

F1 = 2 * (precision * recall) / (precision + recall)
print("the F1 score with NB is: %f" %F1)
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
params_tree = { "min_samples_split":[2, 5, 10, 20],
                "criterion": ('gini', 'entropy')}
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

### D-1: Using Suport Vector Machine
#from sklearn.svm import SVC


clf_SVC = SVC()
clf_SVC.fit(features_train, labels_train)
score = metrics.accuracy_score(labels_test, clf_SVC.predict(features_test))
print("Accuracy with SVM: %f" % score)
recall= recall_score(labels_test, clf_SVC.predict(features_test))
print("recall with SVM: %f" %recall)
precision = precision_score(labels_test, clf_SVC.predict(features_test))
print("precision with SVM: %f" %precision)


F1 = 2 * (precision * recall) / (precision + recall)
print("the F1 score with SVM is: %f" %F1)
print("=========================================")


### D-2: tuning SVM Classifier by scalling the features
clf_SVC = SVC()
params_svm = {"C": [0.5, 1, 5, 10, 100, 10**10],
                        "tol":[10**-1, 10**-10],
                        "class_weight":['auto']
classifier1 = GridSearchCV(clf_SVC, params_svm)
scaler = preprocessing.MinMaxScaler()
Scale_features_train = scaler.fit_transform(features_train)
Scale_features_test = scaler.fit_transform(features_test)

classifier1.fit(Scale_features_train, labels_train)
score = metrics.accuracy_score(labels_test, classifier1.predict(Scale_features_test))
print("Accuracy of scalled features with SVM: %f" % score)
recall= recall_score(labels_test, classifier1.predict(Scale_features_test))
print("recall of scalled features with SVM: %f" %recall)
precision = precision_score(labels_test, classifier1.predict(Scale_features_test))
print("precision of scalled features with SVM: %f" %precision)

F1 = 2 * (precision * recall) / (precision + recall)
print("the F1 score of scalled features with SVM is: %f" %F1)

print("=========================================")


################## Task 5: Select the Best classifiers ########################3

# from the scores for all the above classifiers, NB got the best scores amoge others. 
print("=================LR========================")

test_classifier(clf_LR, my_dataset, features_list)

print("==================NB=======================")

test_classifier(clf_NB, my_dataset, features_list)

print("================DT - 1=========================")

test_classifier(clf_DT, my_dataset, features_list)

print("================DT - 2=========================")

test_classifier(classifier4, my_dataset, features_list)

print("===================SVM 1 ======================")

test_classifier(clf_SVC, my_dataset, features_list)


print("====================SVM 2 =====================")

test_classifier(classifier1, my_dataset, features_list)




# dump the best classifier, dataset and features_list so
# anyone can run/check your results

dump_classifier_and_data(clf_NB, my_dataset, my_best_feature_list)