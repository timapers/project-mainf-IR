import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd

category = {
    1: 0,
    #2: 1,
    10: 1,
    #15: 3,
    17: 2,
    #18: 2,
    #19: 6,
    #20: 7,
    #21: 3,
    22: 3,
    23: 4,
    24: 5,
    25: 6,
    26: 7,
    27: 8,
    28: 9,
    #29: 16
}

confusion_labels = list(category.keys())

data = [[252, 51, 0, 0, 26, 39, 137, 14, 33, 33], [21, 950, 0, 0, 38, 31, 145, 30, 56, 34], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [41, 119, 0, 0, 436, 68, 276, 89, 216, 98], [45, 131, 0, 0, 83, 405, 321, 106, 101, 69], [121, 290, 0, 0, 98, 133, 1258, 147, 190, 139], [21, 51, 0, 0, 34, 43, 170, 504, 23, 52], [16, 89, 0, 0, 83, 34, 176, 13, 945, 60], [24, 44, 0, 0, 38, 37, 82, 25, 48, 518]]
ax = sns.heatmap(data, linewidth=0.5, annot=True, fmt='')
ax.set_title('Confusion Matrix')
ax.set_xlabel("Target")
ax.set_ylabel("Prediction")
ax.set_xticklabels(confusion_labels)
ax.set_yticklabels(confusion_labels)
plt.savefig('../results/confusion_matrix.png')

