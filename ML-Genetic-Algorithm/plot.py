import matplotlib.pyplot as plt
import pandas as pd
import os
a = [s for s in os.listdir("Analys")
	if os.path.isfile(os.path.join("Analys", s))]
a.sort(key=lambda s: os.path.getmtime(os.path.join("Analys", s)))



if a[-1] != 'desktop.ini':
	df = pd.read_excel('Analys/{}'.format(a[-1]))
	print("opening", a[-1])
else:
	df = pd.read_excel('Analys/{}'.format(a[-2]))
	print("opening", a[-2])

generation = df["Generation"].values
bestScore = df["Best Score"].values
avgScore= df["Average Score"].values


x1, = plt.plot(generation, bestScore, label='High Score')
x2, = plt.plot(generation, avgScore, label='Average Score')
plt.xlabel('Generation')
plt.ylabel('Score')
plt.legend(handles=[x1, x2])



plt.show()