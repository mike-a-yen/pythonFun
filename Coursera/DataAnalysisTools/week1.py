import pandas as pd
import numpy as np
from scipy import stats
from itertools import permutations

def ConvertToNan(x,value=999):
    if x == value:
        return np.nan
    else:
        return x

df = pd.read_csv('nesarc_pds.csv')
dependent = 'S1Q24LB'
# Weight in lbs
independent = 'REGION'
# Census Region
# 1. Northeast
# 2. Midwest
# 3. South
# 4. West
#df[dependent] = df[dependent].apply(ConvertToNan)
df[dependent] = df[dependent].replace(999,np.nan)
df = df.dropna(subset=[dependent])

t1 = df[df[independent]==1]
t2 = df[df[independent]==2]
t3 = df[df[independent]==3]
t4 = df[df[independent]==4]
perms = permutations([t1,t2,t3,t4],r=2)
print 'Regions    p-value'
for perm in perms:
    f,p = stats.f_oneway(perm[0][dependent],perm[1][dependent])
    print perm[0][independent], perm[1][independent],'    ',p

results = pd.DataFrame(df[independent].unique(), columns=[independent])
results['mean'] = results[independent].apply(lambda r: df[df[independent]==r][dependent].mean(skipna=True))
results['std'] = results[independent].apply(lambda r: df[df[independent]==r][dependent].std(skipna=True))
