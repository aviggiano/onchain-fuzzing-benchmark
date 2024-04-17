import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
data = pd.read_csv('/tmp/results.csv')

# Create a unique identifier for each 'name' and 'seq' combination
data['group'] = data['name'] + '_' + data['seq'].astype(str)

# Define color palettes for 'local' and 'remote'
local_palette = sns.light_palette("blue", n_colors=len(data[data['name'] == 'local']['seq'].unique()))
remote_palette = sns.light_palette("red", n_colors=len(data[data['name'] == 'remote']['seq'].unique()))

max_value = 1000000
data['fuzzing'] = (data['fuzzing'] / max_value) * 100
data['time'] = (data['time'] // 3000) * 3

# Map each group to a specific color
group_colors = {}
for (name, seq), group in data.groupby(['name', 'seq']):
    if name == 'local':
        # Use index of unique seqs within 'local' to determine shade
        index = list(data[data['name'] == 'local']['seq'].unique()).index(seq)
        group_colors[name + '_' + str(seq)] = local_palette[index]
    else:
        # Use index of unique seqs within 'remote' to determine shade
        index = list(data[data['name'] == 'remote']['seq'].unique()).index(seq)
        group_colors[name + '_' + str(seq)] = remote_palette[index]

# Set up the plotting environment
plt.figure(figsize=(16, 10))
sns.set(style="whitegrid")

# Plotting all groups on the same chart
sns.lineplot(x='time', y='fuzzing', hue='group', data=data, palette=group_colors, marker='o', legend='full')

# Set the plot labels and title
plt.title('Fuzzing x Time')
plt.xlabel('Time (s)')
plt.ylabel('Fuzzing (%)')
plt.legend(title='Groups', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.tight_layout(rect=[0, 0, 1, 1])  # Adjust the rect if the legend still overlaps

# Save the plot to a file
plt.savefig('/tmp/results.png', dpi=300)

# Show the plot
plt.show()

