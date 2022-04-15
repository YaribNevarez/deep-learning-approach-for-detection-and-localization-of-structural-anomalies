import matplotlib.pyplot as plt
import numpy as np

fig, (ax1, ax2) = plt.subplots(2, 1)

fig.suptitle('Performance')

#Python:
begin   = np.array([0.000, 0.002, 0.005, 0.037, 6.991, 10.562, 14.127, 16.457, 16.460, 16.680, 21.104, 22.095, 23.080, 23.725, 23.727, 23.987, 24.978, 25.257, 25.531, 25.710, 25.727, 27.139, 27.886, 27.899, ])
#latency = np.array([27.904, 6.986, 0.038, 6.925, 3.569, 3.562, 2.328, 4.645, 0.247, 4.413, 0.989, 0.984, 0.643, 1.251, 0.270, 0.985, 0.277, 0.273, 0.177, 0.016, 1.410, 0.745, 0.011, 0.003, ])
latency = np.array([50, 6.986, 0.038, 6.925, 3.569, 3.562, 2.328, 4.645, 0.247, 4.413, 0.989, 0.984, 0.643, 1.251, 0.270, 0.985, 0.277, 0.273, 0.177, 0.016, 1.410, 0.745, 0.011, 0.003, ])
event   = ["MODEL", "CONV_2D", "DELEGATE", "HARDWARE", "MUL", "ADD", "MAX_POOL_2D", "CONV_2D", "DELEGATE", "HARDWARE", "MUL", "ADD", "MAX_POOL_2D", "CONV_2D", "DELEGATE", "HARDWARE", "MUL", "ADD", "MAX_POOL_2D", "RESHAPE", "FULLY_CONNECTED", "FULLY_CONNECTED", "FULLY_CONNECTED", "LOGISTIC", ]
colors  = ["#1864ab", "#4a98c9", "#6faed4", "#94c4df", "#4a98c9", "#4a98c9", "#4a98c9", "#4a98c9", "#6faed4", "#94c4df", "#4a98c9", "#4a98c9", "#4a98c9", "#4a98c9", "#6faed4", "#94c4df", "#4a98c9", "#4a98c9", "#4a98c9", "#4a98c9", "#4a98c9", "#4a98c9", "#4a98c9", "#4a98c9", ]

data = [[0.003, 112.330, 115.901, 119.466, 121.811, 334.926, 335.917, 336.903, 337.545, 384.146, 384.426, 384.700, 384.880, 384.897, 386.310, 387.058, 387.072, ],
        [ 112.325, 3.568, 3.563, 2.343, 213.112, 0.989, 0.984, 0.640, 46.598, 0.278, 0.273, 0.178, 0.016, 1.410, 0.746, 0.011, 0.003, ],
        [ 6.925, 0.000, 0.000, 0.000, 4.413, 0.000, 0.000, 0.000, 0.985, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, ]]
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