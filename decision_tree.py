# -*- coding: utf-8 -*-
"""

@author: jgapper
"""

from math import log

my_data = [['Sunny', 'Hot', 'High', 'Weak', 'No'],
 ['Sunny', 'Hot', 'High', 'Strong', 'No'],
 ['Overcast', 'Hot', 'High', 'Weak', 'Yes'],
 ['Rain', 'Mild', 'High', 'Weak', 'Yes'],
 ['Rain', 'Cool', 'Normal', 'Weak', 'Yes'],
 ['Rain', 'Cool', 'Normal', 'Strong', 'No'],
 ['Overcast', 'Cool', 'Normal', 'Strong', 'Yes'],
 ['Sunny', 'Mild', 'High', 'Weak', 'No'],
 ['Sunny', 'Cool', 'Normal', 'Weak', 'Yes'],
 ['Rain', 'Mild', 'Normal', 'Weak', 'Yes'],
 ['Sunny', 'Mild', 'Normal', 'Strong', 'Yes'],
 ['Overcast', 'Mild', 'High', 'Strong', 'Yes'],
 ['Overcast', 'Hot', 'Normal', 'Weak', 'Yes']]

class dtree:
    def __init__(self,attr=-1,value=None,outcome=None,IS=None,IS_NOT=None):
        self.attr=attr
        self.value=value
        self.outcome=outcome 
        self.IS=IS
        self.IS_NOT=IS_NOT

def entropy(obsvs):
    #entropy method
    outcome=counts(obsvs)
    ent=0.0
    for r in outcome.keys():
        p=float(outcome[r])/len(obsvs) #class probability
        ent=ent-p*(log(p)/log(2)) #entropy
    return ent

def subset_data(obsvs,attribute,value):
    #subset based on splits
    subset_fxn=lambda obs:obs[attribute]==value
    subset_1=[obs for obs in obsvs if subset_fxn(obs)]
    subset_2=[obs for obs in obsvs if not subset_fxn(obs)]
    return (subset_1,subset_2)

def counts(obsvs):
#counts of outcome
    outcome={}
    for obs in obsvs:
        r=obs[len(obs)-1] # exclude target variable
        if r not in outcome: outcome[r]=0
        outcome[r]+=1
    return outcome

def buildtree(obsvs):
    if len(obsvs) == 0: return dtree()
    entropy_value = entropy(obsvs)
    gain_flag = 0.0
    attribute = None
    split_sets = None
    attribute_count = len(obsvs[0]) - 1 #remove target variable
    for attr in range(0, attribute_count):
        #find all values for each attribute
        attribute_values = set([obs[attr] for obs in obsvs])
        #iterate through attribute values to calculate each possible gain
        for value in attribute_values:
            subset_1, subset_2 = subset_data(obsvs, attr, value)
            p = float(len(subset_1)) / len(obsvs)
            # Calculate information gain            
            gain = entropy_value - p*entropy(subset_1) - (1-p)*entropy(subset_2)
            #implement flag for greatest gain
            if gain > gain_flag and len(subset_1) > 0 and len(subset_2) > 0:
                gain_flag = gain
                attribute = (attr, value)
                split_sets = (subset_1, subset_2)
    if gain_flag > 0:
        #build tree based on gain flag splits
        IS_Branch = buildtree(split_sets[0])
        IS_NOT_Branch = buildtree(split_sets[1])
        return dtree(attr=attribute[0], value=attribute[1],
                IS=IS_Branch, IS_NOT=IS_NOT_Branch)
    else:
        return dtree(outcome=counts(obsvs))

def printtree(tree,indent='	'):
    # Print the tree with indentation (leaf nodes)
    if tree.outcome!=None:
        print str(tree.outcome)
    else:
    # Print splits
        print '\n Variable: '+str(tree.value)
        print indent+'IS '+str(tree.value),
        printtree(tree.IS,indent+'  ')
        print indent+'IS NOT '+str(tree.value),
        printtree(tree.IS_NOT,indent+'  ')

printtree(buildtree(my_data))