#!/usr/bin/python


from sklearn.feature_selection import SelectFromModel, SelectKBest


##############################################
###Suggestion from the reviwer 1. ############
##############################################


""" reat work on writing auxiliary methods to help in the process of selecting
features! My only suggestion here would be to move this method to 
a separate file to improve readability!
"""  

'''  modified from the original post on :
# https://discussions.udacity.com/t/project-identify-fraud-from-enron-email/259175
'''



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


features_financial =['salary', 'deferral_payments', 'total_payments', 
 'loan_advances', 'bonus', 'restricted_stock_deferred', 
 'deferred_income', 'total_stock_value', 'expenses', 
 'exercised_stock_options', 'other', 'long_term_incentive', 
 'restricted_stock', 'director_fees']
    
NAN_value = 'NaN'

def create_add_features(data_dict, features_list, financial_log=False):
    """
    Given the data dictionary of people with features, adds some features to
    """
    for name in data_dict:

        # If feature is financial, add another variable with log transformation.
        if financial_log:
            for feat in features_financial:
                try:
                    data_dict[name][feat + '_log'] = Math.log(data_dict[name][feat] + 1)
                except:
                    data_dict[name][feat + '_log'] = NAN_value
    # print "finished"
    return data_dict