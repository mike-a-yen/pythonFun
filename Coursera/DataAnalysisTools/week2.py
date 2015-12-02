'''
Compare whether or not being single or married
is related to where you live
'''
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency as chi2
from statsmodels.stats.multicomp import MultiComparison as mc
import itertools as it
import matplotlib.pyplot as plt

# Census Region
# 1. Northeast
# 2. Midwest
# 3. South
# 4. West
region_map = {1:'Northeast',
              2:'Midwest',
              3:'South',
              4:'West'}
independent = 'REGION'
#Current Marital Status
# 1. Married
# 2. Living with someone as if married
# 3. Widowed
# 4. Divorced
# 5. Separated
# 6. Never Married
dependent = 'MARITAL'

data = pd.read_csv('nesarc_pds.csv',usecols=[independent, dependent])
# Since I only want married or single
# replace 1 and 2 with 0,
# and 3-6 with 1
# 0 depicts married
# 1 depicts single
recode = {1:0, 2:0, 3:1, 4:1, 5:1, 6:1}
data[dependent] = data[dependent].map(recode)

# create crosstab to compare across all
# independent variable values
ct = pd.crosstab(data[dependent],data[independent])
results = chi2(ct)
print '*'*30
print '-'*30
print 'Chi2: ',results[0]
print 'p-value: ',results[1]
print 'dof: ',results[2]
print '-'*30
print '*'*30+'\n'

# set confidence limit at 0.05
cl = 0.05
# get all permutations of length 2
# of the independent variable
permutations = list(it.combinations(ct,r=2))

print 'Adjusting for Bonferroni.....'
print '='*40
print '-'*40
print 'limit p-value: ',cl/len(permutations)

# initialize comparison table
# this will be what I print at
# the end to summarize the results
comparison = pd.DataFrame(np.zeros([len(permutations),
                                   len(data[independent].unique())]),
                          columns = ['Region1',
                                     'Region2',
                                     'p-value',
                                     'reject'] )
# complete chi2 comparison for all
# permutations of independent variable
for i,perm in enumerate(permutations):
    subset = data[np.in1d(data[independent],perm)]
    ct = pd.crosstab(subset[dependent],subset[independent])
    results = chi2(ct)
    pv = results[1]
    comparison.loc[i]['Region1'] = perm[0]
    comparison.loc[i]['Region2'] = perm[1]
    comparison.loc[i]['p-value'] = pv
    if pv <= cl/len(permutations):
        comparison.loc[i]['reject'] = True
    else:
        comparison.loc[i]['reject'] = False
print '-'*40
# convert region number code back to name
comparison['Region1'] = comparison['Region1'].map(region_map)
comparison['Region2'] = comparison['Region2'].map(region_map)

print comparison
