import scipy.stats
import numpy as np

mean = 30
std = 4
norm = scipy.stats.norm
pdf = norm.pdf
cdf = norm.cdf

# x < 40
print norm.cdf(40,mean,std)

# x > 21
print 1-norm.cdf(21,mean,std)

# 30 < x < 35
print norm.cdf(35,mean,std)-norm.cdf(30,mean,std)
