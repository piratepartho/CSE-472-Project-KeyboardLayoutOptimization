import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('fitness_info.csv')
#take first 15 rows()
df = df.head(15)

generation = df['generation']
fitness = df['fitness']

df2=pd.read_csv('fitness_info_cnn.csv')
generation_cnn = df2['generation']
fitness_cnn = df2['fitness']

#plot for both models
plt.plot(generation, fitness, marker='o', label='Dense')
plt.plot(generation_cnn, fitness_cnn, marker='o', label='CNN')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.title('Fitness per Generation')
plt.legend()
plt.xticks(range(min(generation), max(generation)+1, 1))
plt.savefig('fitness_plot_comparison_bangla.png')


# plt.plot(generation, fitness, marker='o')

# plt.xlabel('Generation')
# plt.ylabel('Fitness')
# plt.title('Fitness per Generation')

# plt.xticks(range(min(generation), max(generation)+1, 1))
# plt.savefig('fitness_plot_bangla.png')

# plt.show()