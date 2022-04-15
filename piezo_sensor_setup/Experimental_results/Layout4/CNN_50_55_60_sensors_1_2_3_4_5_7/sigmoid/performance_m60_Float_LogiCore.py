import matplotlib.pyplot as plt
import numpy as np

fig, (ax1, ax2) = plt.subplots(2, 1)

fig.suptitle('Performance')

#Python:
begin   = np.array([0.000, 0.002, 0.006, 0.037, 12.555, 16.127, 19.691, 22.020, 22.023, 22.243, 38.640, 39.632, 40.617, 41.262, 41.264, 41.524, 45.118, 45.397, 45.672, 45.850, 45.867, 47.279, 48.026, 48.039, ])
#latency = np.array([48.044, 12.551, 0.038, 12.489, 3.569, 3.562, 2.328, 16.618, 0.247, 16.387, 0.990, 0.983, 0.643, 3.855, 0.270, 3.588, 0.278, 0.273, 0.177, 0.016, 1.410, 0.745, 0.011, 0.003, ])
latency = np.array([50, 12.551, 0.038, 12.489, 3.569, 3.562, 2.328, 16.618, 0.247, 16.387, 0.990, 0.983, 0.643, 3.855, 0.270, 3.588, 0.278, 0.273, 0.177, 0.016, 1.410, 0.745, 0.011, 0.003, ])
event   = ["MODEL", "CONV_2D", "DELEGATE", "HARDWARE", "MUL", "ADD", "MAX_POOL_2D", "CONV_2D", "DELEGATE", "HARDWARE", "MUL", "ADD", "MAX_POOL_2D", "CONV_2D", "DELEGATE", "HARDWARE", "MUL", "ADD", "MAX_POOL_2D", "RESHAPE", "FULLY_CONNECTED", "FULLY_CONNECTED", "FULLY_CONNECTED", "LOGISTIC", ]
colors  = ["#1864ab", "#4a98c9", "#6faed4", "#94c4df", "#4a98c9", "#4a98c9", "#4a98c9", "#4a98c9", "#6faed4", "#94c4df", "#4a98c9", "#4a98c9", "#4a98c9", "#4a98c9", "#6faed4", "#94c4df", "#4a98c9", "#4a98c9", "#4a98c9", "#4a98c9", "#4a98c9", "#4a98c9", "#4a98c9", "#4a98c9", ]

data = [[0.003, 112.248, 115.819, 119.384, 121.731, 334.864, 335.856, 336.842, 337.484, 384.079, 384.359, 384.633, 384.813, 384.831, 386.244, 386.992, 387.005, ],
        [ 112.243, 3.568, 3.563, 2.345, 213.130, 0.990, 0.984, 0.640, 46.593, 0.278, 0.273, 0.178, 0.016, 1.411, 0.746, 0.011, 0.003, ],
        [ 12.489, 0.000, 0.000, 0.000, 16.387, 0.000, 0.000, 0.000, 3.588, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, ]]
columns = ("CONV_2D", "MUL", "ADD", "MAX_POOL_2D", "CONV_2D", "MUL", "ADD", "MAX_POOL_2D", "CONV_2D", "MUL", "ADD", "MAX_POOL_2D", "RESHAPE", "FULLY_CONNECTED", "FULLY_CONNECTED", "FULLY_CONNECTED", "LOGISTIC", )

ax1.barh(range(len(begin)),  latency, left=begin, color=colors)
ax1.grid(linestyle = ':')


plt.sca(ax1)
plt.yticks(range(len(begin)), event)
ax1.tick_params(axis='both', which='major', labelsize=5)
ax1.tick_params(axis='both', which='minor', labelsize=1)

plt.xlabel("Schedule (ms)")
plt.ylabel("Task")

rows = ["Hardware", "Software", "II OFFSET"]

# Get some pastel shades for the colors
colors = plt.cm.Blues(np.linspace(0.4, 0.8, len(rows)))
n_rows = len(data)

index = np.arange(len(columns)) + 0.3
bar_width = 0.4

# Initialize the vertical-offset for the stacked bar chart.
y_offset = np.zeros(len(columns))

# Plot bars and create text labels for the table
cell_text = []
for row in range(n_rows):
    ax2.bar(index, data[row], bar_width, bottom=y_offset, color=colors[row])
    y_offset = y_offset + data[row]
    cell_text.append(data[row])
# Reverse colors and text labels to display the last value at the top.
colors = colors[::-1]
cell_text.reverse()

plt.sca(ax2)
# Add a table at the bottom of the axes
the_table = ax2.table(cellText=cell_text,
                      rowLabels=rows,
                      rowColours=colors,
                      colLabels=columns,
                      loc='bottom',
                      fontsize='xx-small')

the_table.auto_set_font_size(False)
the_table.set_fontsize(7)


# Adjust layout to make room for the table:

plt.subplots_adjust(left=0.2, bottom=0.2)

plt.ylabel("Latency (ms)")

plt.xticks([])
ax2.grid(linestyle = ':')


plt.show()