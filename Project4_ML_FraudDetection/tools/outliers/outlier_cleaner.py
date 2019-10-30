#!/usr/bin/python

''' this code is from ://github.com/jdamiani27/Intro-to-Machine-Learning/blob/master/ 
I used this and also http://napitupulu-jon.appspot.com/posts/outliers-ud120.html
to understand the outliers and how it affects the dataset to do deal with it in my project

'''
def outlierCleaner(predictions, ages, net_worths):
    """
        clean away the 10% of points that have the largest
        residual errors (different between the prediction
        and the actual net worth)

        return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error)
    """
    
    cleaned_data = zip(ages, net_worths, [(float(pred) - actual)**2 for pred, actual in zip(predictions, net_worths)])

    cleaned_data.sort(key = lambda tup: tup[2])

    for i in range(0, int(len(cleaned_data) * 0.1)):
        cleaned_data.pop()
    
    return cleaned_data

