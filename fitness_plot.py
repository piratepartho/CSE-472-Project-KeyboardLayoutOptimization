import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('fitness_info.csv')

generation = df['generation']
fitness = df['fitness']


plt.plot(generation, fitness, marker='o')

plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.title('Fitness per Generation')

plt.xticks(range(min(generation), max(generation)+1, 1))
plt.savefig('fitness_plot.png')

plt.show()