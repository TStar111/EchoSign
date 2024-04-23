import torch
import pandas as pd
from sklearn.metrics import confusion_matrix
from models_NN import SimpleNN2
import matplotlib.pyplot as plt
import numpy as np

input_dim = 28
hidden_dim=128
output_dim = 11

# Load your PyTorch model
model = torch.load("models/rs_comp.pt")
# Initialize model with saved weights
model = SimpleNN2(input_dim, hidden_dim, output_dim)

# Load the model checkpoint
checkpoint = torch.load("models/rs_comp.pt")

# Load the model state_dict
model.load_state_dict(checkpoint)

# Set the model to evaluation mode
model.eval()

# Load your CSV file containing the data
data = pd.read_csv("data/dataset_double_word/rs_comp.csv")

# Assuming your last column is the label and the preceding columns are features
features = data.iloc[:, :-1].values.astype(float)
labels = data.iloc[:, -1].values

predicted_labels = []

# Iterate over the data and run predictions using the model
with torch.no_grad():
    for feature in features:
        # Convert features to tensor
        input_tensor = torch.tensor(feature).float().unsqueeze(0)  # Add batch dimension
        # Perform inference
        output = model(input_tensor)
        predicted_label = output.argmax().item()  # Get the index of the class with the highest probability
        predicted_labels.append(predicted_label)

# Compute the confusion matrix
cm = confusion_matrix(labels, predicted_labels)

# Print or visualize the confusion matrix as desired
print("Confusion Matrix:")
print(cm)

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
