'''
Compare the weight of males and females
in the four major regions of the US
Determine if there is a statistical 
significance in weight difference between
the regions
'''
import pandas as pd
import numpy as np
from scipy import stats
from itertools import permutations

# Weight in lbs
dependent = 'S1Q24LB'
# Census Region
# 1. Northeast
# 2. Midwest
# 3. South
# 4. West
independent = 'REGION'

# Read Data
df = pd.read_csv('nesarc_pds.csv',usecols=[independent,dependent])
# Replace all values of 999 with nan
# values of 999 are unrecorded
df[dependent] = df[dependent].replace(999,np.nan)
# drop all entries with nan in dependent column
df = df.dropna(subset=[dependent])

# subset data by independent value
t1 = df[df[independent]==1]
t2 = df[df[independent]==2]
t3 = df[df[independent]==3]
t4 = df[df[independent]==4]
# get all permutations of subsets with length of 2
perms = [p for p in permutations([t1,t2,t3,t4],r=2)]
# Initialize comparison data frame,
# will contain regions in comparison,
# p_values, f_values,
# and preferred null or alternative
compare = pd.DataFrame([(r[0][independent].unique()[0],r[1][independent].unique()[0])
                        for r in perms],
                       columns=['region1','region2'])
compare['p_value'] = np.zeros(len(compare))
compare['f_value'] = np.zeros(len(compare))
compare['result'] = ['NA']*len(compare)
# Set confidence limit to 5%
cl = 0.05
for i,perm in enumerate(perms):
    f,p = stats.f_oneway(perm[0][dependent],
                         perm[1][dependent])
    compare.loc[i,['f_value','p_value']] = f,p
    if p <= cl:
        compare.loc[i,'result']='ALT'
    else:
        compare.loc[i,'result']='NULL'

print compare

summary = df.groupby([independent])
print summary.describe()

# Doing the comparison perm by perm
# increase the type 1 error rate,
# so this is not a good way to
# calculate p-values. Instead we
# would like to calculate all of the
# p-values at once, using a 3rd party
# algorithm
import statsmodels.formula.api as smf
import statsmodels.stats.multicomp as multi

multicomp = multi.MultiComparison(df[dependent],df[independent])
res = multicomp.tukeyhsd()
print res.summary()
