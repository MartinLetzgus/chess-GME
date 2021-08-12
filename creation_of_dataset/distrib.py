import collections
import pickle
import numpy as np
import matplotlib.pyplot as plt

def mean_elo(game):
    return((game['white']['rating']+game['black']['rating'])/2)

games = pickle.load( open( "martinovichev.p", "rb" ))  
elos = []

for game in (games):
    elos.append(mean_elo(game))

pickle.dump(games, open( "martinovichev.p", "wb" ) )

print(len(games))
    
array = np.array(elos)
bins = np.arange(0,3500,100)
hist = np.histogram(array, bins=bins)
print(hist)
plt.hist(array, bins=bins)
plt.show()