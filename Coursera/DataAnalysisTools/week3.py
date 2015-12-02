'''
This time I am looking at how the depth of
a crater on mars is related to the diameter
of the crater.
'''
import numpy as np
import pandas as pd
import scipy.stats as stats
import itertools as it
import matplotlib.pyplot as plt

#load crater data
f_name = 'marscrater_pds.csv'
dependent = 'DIAM_CIRCLE_IMAGE'
independent = 'DEPTH_RIMFLOOR_TOPOG'
df = pd.read_csv(f_name,usecols=[independent,dependent])
# usecols saves time loading
# drop all nans
df = df.dropna()

# compute pearsonr
pr = stats.pearsonr(df[independent], df[dependent])
print '-'*40
print 'From pearsonR'
print '='*40
print 'Correlation Coefficient    p-value'
print '_'*40
print str(pr[0])+'        '+str(pr[1])
print '='*40

# generate linear regression through
# the data, this helps visualize the
# linearness of the data
regress = stats.linregress(df[independent],df[dependent])
y = lambda x: regress[0]*x + regress[1]
# labels of linregress return
labels = ['slope', 'intercept', 'r_value', 'p_value', 'std_err']
# print output from linregress
print '-'*40
print 'From linregress'
print '='*40
for v,k in zip(regress,labels):
    print k+':    '+str(v)
print 'r2:        '+str(regress[2]**2)
print '='*40

# make scatter plot
# and plot linear fit
fig,ax = plt.subplots()
# set alpha less than 1 since many data points overlap
ax.scatter(df[independent],df[dependent],edgecolor='none',alpha=0.1)
ax.plot(df[independent],y(df[independent]), color='red')
ax.set_xlabel(independent)
ax.set_ylabel(dependent)
plt.show()
fig.savefig('week3_results.png')
