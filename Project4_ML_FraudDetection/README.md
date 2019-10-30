### PRojects report
# Yasser Alnakhli 
poi_id_3.py
### Project and Dataset overview:
Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. As part of your answer, give some background on the dataset and how it can be used to answer the project question. Were there any outliers in the data when you got it, and how did you handle those?  [relevant rubric items: “data exploration”, “outlier investigation”]

Enron was one of the biggest  energy companies in the US back in early 2000. In 2002, this company which based in Huston, experienced the biggest audit failure which led to the company collapse because of widespread corporate fraud [1]. 

This project is about using the machine learning skills to investigate Enron employees who may get involved in the fraud(named as Person Of Interest, POI) . A public dataset has been generated as a result of a federal investigation will help to do this project. The dataset include many emails and different financial data for top exclusive and other information. The Udacity lessons and mini projects obtained different information to help in this project. A dataset with 146 data points were given each has 21 features. The features are in 3 main categories. Finical features (in US dollars), email features (as text  string) and POI label (the main feature represented as integer). It is also shown from the dataset that only 18 person out of the 146 are POI. Thus, using Machine Learning to identity the POI is very helpful as the complexity of the dataset. 

### Suggestion from the reviewer “remove more CLEAR outliers”
The dataset contains some outliers. One very clear outlier is the “TOTAL” which was the sum of the other points .Look at enron61702insiderpay.pdf for more info. “Lockhart Eugene E” has also no values, so it has been considered as another outlier. Finally “The Travel Agency in the Park” has no sense of the the current data. It might be an entry error. So it has been also considered as an outlier. They have  been removed by using data_dict.pop(). Dealing with the outlier in this dataset is very critical as the limited amount of the data and to keep the limited target class that the data include. Thus, only the above outliers will be removed and we can not mark other outliers using common plotting techniques.  I thought it would be better to keep other data as it is after removing those and see how my model goes. 

### Required from the reviewer “mention the NaNs”
At the dataset, particularly some features contain some missing values. NaNs represent missing values and it might be entry errors or Not Applicable filed to be filled. It should be addressed as some algorithms find them difficult to deal with such data. It has been replaced by 0 in the code. Moreover, featureFormat() at feature_format.py converts dictionary to numpy array of features remove_NaN = True will convert "NaN" string to 0.0. This also has been used as a tool for this project.


### Feature Selections:
What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? As part of the assignment, you should attempt to engineer your own feature that does not come ready-made in the dataset -- explain what feature you tried to make, and the rationale behind it. (You do not necessarily have to use it in the final analysis, only engineer and test it.) In your feature selection step, if you used an algorithm like a decision tree, please also give the feature importances of the features that you use, and if you used an automated feature selection function like SelectKBest, please report the feature scores and reasons for your choice of parameter values.  [relevant rubric items: “create new features”, “intelligently select features”, “properly scale features”]

Required from the reviewer “Add new features and discuss if they have impact to the model”
New features
With logarithmic transformation, some new features were added to the Financial variables. This is because we th financial aspects of the POIs are non liner. Hopefully this will improve the algorithm.
  new_features = [ "log_total_payments", "log_bonus", "log_salary","log_total_stock_value"]
The above features were log transformed using numpy log method. Unfortunately, adding those new features did not make any significant changes the algorithm performance. This was clear when I run the program before and after adding the features. 
I run both (Before adding features and after) and test it with tester.py and I got the following: 
Before:
16 best features: ['salary', 'to_messages', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus', 'director_fees', 'total_stock_value', 'shared_receipt_with_poi', 'from_poi_to_this_person', 'exercised_stock_options', 'other', 'from_this_person_to_poi', 'deferred_income', 'expenses', 'restricted_stock']

Classifier
Accuracy
Precision
Recall
F1
LogisticRegression()
0.78420
0.18003
0.17400	
0.17696
naive_bayes as GaussianNB() &
0.73827
 0.22626
0.39800	
0.28851
naive_bayes as GaussianNB() $
0.73900
0.22604
0.39500	
 0.28753
naive_bayes as BernoulliNB() &
0.71840
0.29121
0.77550
0.42342
DecisionTreeClassifier()
0.79733
0.22632
0.21500
0.22051
DecisionTreeClassifier()   $  & *
0.84973
0.30462
0.09900	
0.14943
neural_network by MLPClassifier.() 
 0.65047
0.12750
0.27750	
0.17472
neural_network by MLPClassifier.() $
0.65700
0.12763
0.26950
0.17323
neural_network by MLPClassifier.()  & *
 0.84680
0.13835
0.02850	
0.04726

$ With scaled features
& Tunned Parameters 
* took too long to complete the run. About 2 hours

After:
16 best features: ['salary', 'total_stock_value_log', 'total_payments', 'salary_log', 'bonus', 'bonus_log', 'total_stock_value', 'shared_receipt_with_poi', 'exercised_stock_options', 'exercised_stock_options_log', 'total_payments_log', 'deferred_income', 'expenses', 'restricted_stock', 'long_term_incentive', 'loan_advances']

Classifier
Accuracy
Precision
Recall
F1
LogisticRegression()
0.78420
0.18003
 0.17400	
0.17696
naive_bayes as GaussianNB() &
0.73827
0.22626
0.39800	
0.28851
naive_bayes as GaussianNB() $
0.73900
0.22604
0.39500	
0.28753
naive_bayes as BernoulliNB() &
0.72127
0.29358
0.77550
0.42592
DecisionTreeClassifier()
0.79473
0.22489
0.22050
0.22267
DecisionTreeClassifier()   $  &
It took too long time, I just exclude it. But I got the scores from my code not from tester.py and it does not show a significant difference.
neural_network by MLPClassifier.() 
0.66027
0.12627
0.26150	
0.17030
neural_network by MLPClassifier.() $
0.66280
0.12451
0.25350	
0.16700
neural_network by MLPClassifier.()  &
It took too long time, I just exclude it. But I got the scores from my code not from tester.py and it does not show a significant difference. log_trans.docx

$ With scaled features
& Tunned Parameters 

Required from the reviewer “The number of selected features.. Why this number?”
Feature Selections:
As I mentioned above, the dataset has different categories of features. Only all the numeric features were selected at first as well as the main label POI. Then  I narrowed down the number of features using SelectKBest feature selection. After many tries, with more than one algorithm, I found some changes as below. So, 10 features only have been used. check the file feature_number.docx attached. I got confused when using my approach in getting the scores and the tester.py approach. In my approach I get very high scores and the number of features change the scores significantly. Unlike when testing with teaster.py.


Number of Features
Algorithm
Accuracy
Precision
Recall
F1
23
NB
 0.73827
0.22626
0.39800
 0.28851

DT
0.79400
0.22335
0.22000
0.22166

NN
 0.65347
0.12640
0.27050
0.17229
16
NB
 0.73827
0.22626
0.39800
 0.28851

DT
0.79560
0.22554
0.21900
0.2222

NN
0.65607
0.12562
0.26500
0.17045
10
NB
0.85464
0.48876
 0.38050
0.42789

DT
0.79553
0.22514
0.21850
0.22177

NN
 0.65613
0.11805
0.24400
0.15911
6
NB
 0.73827
0.22626
0.39800
 0.28851

DT
0.79753
0.23037
0.22150
0.22585

NN
0.64993
0.11563
0.24450
0.15701



Moreover, feature scaling was also necessary for some features to get better scores for some classifier(support vector machine (SVM) and Decision Tree (DT)). However, nothing has changes  to others [3].

The features I start with:
main_feature = ['poi']

financial_features =['salary', 'deferral_payments', 'total_payments', 
 'loan_advances', 'bonus', 'restricted_stock_deferred', 
 'deferred_income', 'total_stock_value', 'expenses', 
 'exercised_stock_options', 'other', 'long_term_incentive', 
 'restricted_stock', 'director_fees']

The features after SelectKBest are :
10 best features: ['salary', 'total_stock_value_log', 'salary_log', 'bonus', 'bonus_log', 'total_stock_value', 'exercised_stock_options', 'exercised_stock_options_log', 'total_payments_log', 'deferred_income']


























Required from the reviewer “Adding at least one new feature”
Pick an Algorithm:
What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms? [relevant rubric item: “pick an algorithm”]

What does it mean to tune the parameters of an algorithm, and what can happen if you don’t do this well? How did you tune the parameters of your particular algorithm? What parameters did you tune? (Some algorithms do not have parameters that you need to tune -- if this is the case for the one you picked, identify and briefly explain how you would have done it for the model that was not your final choice or a different model that does utilize parameter tuning, e.g. a decision tree classifier). [relevant rubric items: “discuss parameter tuning”, “tune the algorithm”]

Four different classifiers were used including: LogisticRegression(), naive_bayes as GaussianNB(), DecisionTreeClassifier() and neural_network by MLPClassifier.()  A default with the final feature list and hold out were used. The results as following:


Classifier
Accuracy
Precision
Recall
F1
LogisticRegression()
0.78420
0.18003
 0.17400	
0.17696
naive_bayes as GaussianNB() &
0.85464	
0.48876
0.38050	
 0.42789
naive_bayes as GaussianNB() $
0.73900
0.22604
0.39500	
0.28753
naive_bayes as BernoulliNB() &
0.72127
0.29358
0.77550
0.42592
DecisionTreeClassifier()
0.79473
0.22489
0.22050
0.22267
DecisionTreeClassifier()   $  &
It took too long time, I just exclude it. But I got the scores from my code not from tester.py and it does not show a significant difference.
neural_network by MLPClassifier.() 
0.66027
0.12627
0.26150	
0.17030
neural_network by MLPClassifier.() $
0.66280
0.12451
0.25350	
0.16700
neural_network by MLPClassifier.()  &
It took too long time, I just exclude it. But I got the scores from my code not from tester.py and it does not show a significant difference. log_trans.docx

$ With scaled features
& Tunned Parameters 
From the table above, the naive_bayes as Gaussain() was the best classifier to be selected.










Required from the reviewer “mention the tunning step in more details”
Tuning Algorithms:
Setting different parameters or changing then to get the best results out of an algorithm called tunning. Most of the times, although a particular algorithm suits a kind of data the most, if it has not tunned nicely, it wont work as it should be. Thus, it is very important in machine learning to know most of the parameters of each algorithm. Then tying to tune them properly to work efficient.  However, playing around with the tuning step should consider over-fitting the data. It is a common problem at this aspect. It other words, over-fitting refers when training the data too well, here is more information about it [7].
This shown in my model while working with the Decision Tree Algorithm. At the first try of the algorithm, It gave a very poor result. However, after using GridSearchCV() with different parameters params_tree = { "min_samples_split":[2, 5, 10], "criterion": ('gini', 'entropy'), "max_features": ["sqrt", "log2"],  "max_depth":[2, 3], 'min_samples_leaf':[2, 3,5,10]} the performance of the algorithm worked more efficient.  With this tunning I could have tried both gini vs entopy and different minimum numbers of splits  for more information please check ref. [5,6].
“min_samples_split: int, float, optional (default=2)
The minimum number of samples required to split an internal node:
    • If int, then consider min_samples_split as the minimum number.
    • If float, then min_samples_split is a percentage andceil(min_samples_split * n_samples) are the minimum number of samples for each split.”
“criterion : string, optional (default=”gini”)
        ◦ The function to measure the quality of a split. Supported criteria are “gini” for the Gini impurity and “entropy” for the information gain."
“max_features : int, float, string or None, optional (default=None)
The number of features to consider when looking for the best split:
    • If int, then consider max_features features at each split.
    • If float, then max_features is a percentage and int(max_features * n_features) features are considered at each split.
    • If “auto”, then max_features=sqrt(n_features).
    • If “sqrt”, then max_features=sqrt(n_features).
    • If “log2”, then max_features=log2(n_features).
    • If None, then max_features=n_features.
Note: the search for a split does not stop until at least one valid partition of the node samples is found, even if it requires to effectively inspect more than max_features features.”
“max_depth : int or None, optional (default=None)
The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples.”
However, in neural_network , the tuningwas not sucessful. Different parameters have ben used and changes. All did not get better result than the default or just scaling the features. clf_NN= MLPClassifier()  params_NN = {'hidden_layer_sizes': [10, 20],'activation': ['logistic', 'relu'], 'max_iter': [150, 200]}
Another tunning have been done on my algorithm which is in BernoulliNB(). The alpha parameter plays a significant role in enhancing the performance of the NB BernoulliNB(). It totally changes when using very low alpha in regard to a relative high number. Unfortunately there are not many other parameters to tune in this algorithm. I tried my best but in different ways with different features numbers. But I only got the current score. 


Required from the review 3
Well, One important lesson learnt, tunning the classifier based on the best precision and recall plays a significant role in order to get it right. After I applied this to my NB Gaussian(), it gave a nice score for both precision accuracy and recall. 

Validation:
What is validation, and what’s a classic mistake you can make if you do it wrong? How did you validate your analysis? [relevant rubric items: “discuss validation”, “validation strategy”]

In any Machine Learning project, validation is extremely important process where checking the validity of the training model. Splitting the data to training and testing will give a chance to train the model with the training set...A very common error is that training the model to all the dataset which might overfit the model 
Hold out validation has been performed  to split train  by from sklearn.cross_validation import train_test_split.
Evaluation Metrics:
Give at least 2 evaluation metrics and your average performance for each of them. Explain an interpretation of your metrics that says something human-understandable about your algorithm’s performance. [relevant rubric item: “usage of evaluation metrics”]

The best classifier NB Gaussain() got the following scores:
================== NB   Best Estimator   =======================
GaussianNB(priors=None)
	Accuracy: 0.85464	Precision: 0.48876	Recall: 0.38050	F1: 0.42789	F2: 0.39814
	Total predictions: 14000	True positives:  761	False positives:  796	False negatives: 1239	True negatives: 11204


Accuracy with NB:   0.85464
It means that my model has 72% accuracy to predict if the POI or not. However as it has been shown above , accuracy only can not make you sure about the prediction. 

recall with NB:    0.38050
This means that my model has identified  29.6% of the POIs. In other words, this represented how many POIs my model has identified

precision with NB:   0.48876
This means that my model has classified 75% of all people as POIs. In other words, the ratio of truly classified POI/(false classified POI + true classified POI) = 75%.

the F1 score with NB is:   0.42789
The F1 score or as it also known as balanced score or f measure [4]. this is the weighted average of the precision and the recall. 

Problems Faced while doing this project:
    • After I have done most of the mini projects, It was not clear for me how to start the project. What tools should I use and how. I get out of this issue after reading a lot of helpful discussions [2] at the Udacity forums and one-to-one meeting was also very helpful to start up.
    • Many used libraries was not installed. I used my anaconda environment to install most of the libraries. However, I faced some issues with python version (2.7 and 3.x) 
    • The features selection step was also very confusing for me. I decided to use the numeric features as they work nicely with sklearn. It will also take more time to create new features and since the deadline is very soon, I decided to just stick this this numeric features and see how it goes. 
    • Deciding the best classifier to be used. I used many classifiers and I decided to use the one obtained the best scores.
    • The first reviewer has commented some important and useful information. I got confused with hold out and cros validation...
    • After my 1st submission, I had to exclude SVM algorithm. I used MLPClassifier.() instead.
    • Testing my algorithms with tester.py take sometime very long time more than 2 hours. So I decided to change some algorithms as well. 
    • This project is time consuming. I could have done much better job if I have enough time. Working under-stress was a challenge. Holidays time here in my country. My deadline of the nondegree course in the July 8th. All those reasons and more affected my performance.








What else can be done?
    • Include the texture features (email features) beside my numeric features (financial features) 
    • Making new features out of the avilable features to improve the performance of some classifiers. For example log or sqrt some features and add them again to the feature list probably will give better scores 
    • TensorFlow  become more and more famous. I install it to my machine, however, I was not sure if I am able to use it with this project or not. But I think it will give the project more interested outcomes 
    • I would also use PipeLine which allows to stack many transforms and final classifier. GridSearchCV only been used which allows to specify different parameter.


Conclusion:

This project helped me to get the idea of the ML process starting from   data exportation and designing new features which help to make a better prediction. Outliers and how it affect the data is also important lesson. Choosing the right algorithm with the right classifier is also important. Moreover, there are different ways to enhance the performance of any classier. Validation and using more than just one evaluation matrice are also very essential in any ML project. 
 
Machine Learning is very powerful and it can be used in many issues starting with investigation (like this project) or predicting the crimes for example. It is way beyond just suggesting the facebook friends or books in AMAZON. I will definitely use this in healthcare which is my field. I have read a lot about predicting cancer for some patients using ML techniques which have been applied to some bigdata. Image processing and X-ray images to learn the machines to automatically predict a particular disease which will help in diagnosis. Driving car future is also important field and many more.


References:
[1] https://en.wikipedia.org/wiki/Enron_scandal
[2] https://discussions.udacity.com/t/project-fear-strugging-with-machine-learning-project/198529/2
[3] http://machinelearningmastery.com/tactics-to-combat-imbalanced-classes-in-your-machine-learning-dataset/
[4] http://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html
[5] https://www.garysieling.com/blog/sklearn-gini-vs-entropy-criteria
[6] http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
[7]http://machinelearningmastery.com/overfitting-and-underfitting-with-machine-learning-algorithms/
