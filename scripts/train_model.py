import torch
import torch.nn as nn
import pandas as pd
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset
from torch.optim import Adam
import torch.nn.functional as F


def create_and_train_nn_classification(csv_file, model_save_path):
    # Step 1: Load your dataset
    data = pd.read_csv(csv_file)

    # Assuming your dataset has features in columns 1 to n-1 and the target variable in column n
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values

    # Step 2: Split your data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Step 3: Convert your data into PyTorch tensors
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.long)  # Assuming integer labels for classification
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.long)

    # Step 4: Create DataLoader for your datasets
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

    # Step 5: Define your neural network architecture
    class SimpleNN(nn.Module):
        def __init__(self, input_dim, hidden_dim, output_dim):
            super(SimpleNN, self).__init__()
            self.fc1 = nn.Linear(input_dim, hidden_dim)
            self.fc2 = nn.Linear(hidden_dim, output_dim)

        def forward(self, x):
            x = F.relu(self.fc1(x))
            x = self.fc2(x)
            return x

    # Step 6: Instantiate your neural network
    input_dim = X_train.shape[1]
    hidden_dim = 64
    output_dim = len(pd.unique(y))  # Number of unique classes in your target variable
    model = SimpleNN(input_dim, hidden_dim, output_dim)

    # Step 7: Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=0.001)

    # Step 8: Train your neural network
    num_epochs = 10
    for epoch in range(num_epochs):
        for inputs, targets in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
        print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item()}")

    # Step 9: Save your trained model
    torch.save(model.state_dict(), model_save_path)
    print("Model has been saved successfully!")

# TODO: Consider cross-validation
# TODO: Consider wandb for additional insight while training and visualizing convergence.
