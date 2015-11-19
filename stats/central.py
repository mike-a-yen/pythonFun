import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dist = np.random.exponential(scale=10,size=50)

sample_size = 1000 # pick n from dist
nSamples = 100000 # repeat n times
samples = pd.DataFrame([dist[np.random.randint(0,len(dist),sample_size)]
                        for n in np.arange(nSamples)])

samples['mean'] = samples.apply(np.mean, axis=1)
samples['max'] = samples.apply(np.max, axis=1)
samples['min'] = samples.apply(np.min, axis=1)
samples['std'] = samples.apply(np.std, axis=1)
samples['mean'].hist(alpha=0.5)
#samples['max'].hist()
#samples['min'].hist()
samples['std'].hist(alpha=0.5)
plt.show()
