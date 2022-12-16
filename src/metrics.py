import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd
from sklearn.metrics import classification_report

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

data = [[193, 25, 5, 18, 32, 166, 9, 28, 6, 30], [11, 815, 9, 26, 48, 163, 29, 46, 10, 23], [5, 10, 234, 11, 16, 47, 25, 13, 2, 21], [39, 88, 30, 401, 76, 236, 60, 191, 32, 84], [37, 74, 13, 58, 400, 282, 70, 102, 29, 49], [95, 189, 30, 67, 179, 1215, 168, 162, 38, 112], [9, 47, 29, 21, 36, 123, 437, 23, 27, 35], [12, 54, 7, 56, 50, 166, 10, 881, 15, 48], [15, 14, 2, 22, 26, 52, 32, 21, 209, 84], [10, 19, 8, 21, 20, 98, 26, 46, 39, 468]]
ax = sns.heatmap(data, linewidth=0.5, annot=True, fmt='')
ax.set_title('Confusion Matrix')
ax.set_xlabel("Target")
ax.set_ylabel("Prediction")
ax.set_xticklabels(confusion_labels)
ax.set_yticklabels(confusion_labels)
plt.savefig('../results/confusion_matrix.png')

y = []
y_pred = []
for i in range(len(data)):
    for j in range(len(data[i])):
        count = data[i][j]
        for k in range(count):
            y.append(i)
            y_pred.append(j)

confusion_labels =  ["Film & Animation", "Music", "Sports", "People & Blogs", "Comedy", "Entertainment", "News & Politics", "How-to & Style", "Education", "Science & Technology"]

print(classification_report(y, y_pred, target_names=confusion_labels))

