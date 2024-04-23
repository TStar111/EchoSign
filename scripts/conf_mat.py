import matplotlib.pyplot as plt
import numpy as np

# Define your confusion matrix
cm = np.array([[12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # True labels for 'what'
               [0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # True labels for 'time'
               [0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0],   # True labels for 'car'
               [0, 4, 0, 8, 0, 0, 0, 0, 0, 0, 0],   # True labels for 'church'
               [0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0],   # True labels for 'family'
               [0, 0, 0, 0, 0, 11, 1, 0, 0, 0, 0],   # True labels for 'meet'
               [0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0],   # True labels for 'live'
               [0, 0, 0, 0, 0, 0, 2, 10, 0, 0, 0],   # True labels for 'big'
               [0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0],   # True labels for 'more'
               [0, 0, 0, 0, 0, 3, 2, 0, 0, 7, 0],   # True labels for 'but'
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11]]) # True labels for 'none'


true_labels = ['what', 'time', 'car', 'church', 'family', 'meet', 'live', 'big', 'more', 'but', 'none']
# Plot the confusion matrix
plt.figure(figsize=(10, 8))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()

# Add labels
tick_marks = np.arange(len(true_labels))
plt.xticks(tick_marks, true_labels, rotation=45)
plt.yticks(tick_marks, true_labels)

# Add counts in the cells
thresh = cm.max() / 2.
for i, j in np.ndindex(cm.shape):
    plt.text(j, i, format(cm[i, j], 'd'),
             horizontalalignment="center",
             color="white" if cm[i, j] > thresh else "black")

plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.tight_layout()
plt.show()
