import numpy as np
import matplotlib.pyplot as plt

timmy_values = (0.2, 0.8)
johnny_values = (0.5, 0.3)
datum_values = (1, 1)

ind = np.arange(2)  # the x locations for the groups
width = 0.1875        # the width of the bars

fig, ax = plt.subplots()
timmy_bars = ax.bar(ind, timmy_values, width, color='g')
johnny_bars = ax.bar(ind + width, johnny_values, width, color='b')
datum_bars = ax.bar(ind + 2 * width, datum_values, width, color='c')

# add some text for labels, title and axes ticks
ax.set_ylabel('Percentage')
ax.set_title('Bot Similarity Metrics')
ax.set_xticks(ind + width)
ax.set_xticklabels(('   Deck Card Similarity', '   Deck Color Similarity'))

ax.legend((timmy_bars[0], johnny_bars[0], datum_bars[0]), ('Timmy Bot', 'Johnny Bot', 'Datum'))

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

autolabel(timmy_bars)
autolabel(johnny_bars)
autolabel(datum_bars)

plt.show()
