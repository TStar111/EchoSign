import torch
import torch.nn as nn
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from torch.utils.data import DataLoader, TensorDataset
import torch.nn.functional as F
import argparse

def train_with_cross_validation(csv_file, learning_rates, num_splits=5):
    # Step 1: Load your dataset
    data = pd.read_csv(csv_file)
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values

    # Step 2: Convert your data into PyTorch tensors
    X_tensor = torch.tensor(X, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.long)

    # Step 3: Initialize cross-validation
    skf = StratifiedKFold(n_splits=num_splits)

    best_lr = None
    best_avg_loss = float('inf')

    for lr in learning_rates:
        avg_loss = 0.0

        for _, test_index in skf.split(X, y):
            X_test, y_test = X[test_index], y[test_index]
            test_dataset = TensorDataset(torch.tensor(X_test, dtype=torch.float32), 
                                         torch.tensor(y_test, dtype=torch.long))
            test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

            model = SimpleNN(input_dim=X.shape[1], hidden_dim=64, output_dim=len(pd.unique(y)))
            criterion = nn.CrossEntropyLoss()
            optimizer = torch.optim.Adam(model.parameters(), lr=lr)

            model.train()

            for epoch in range(num_epochs):
                for inputs, targets in train_loader:
                    optimizer.zero_grad()
                    outputs = model(inputs)
                    loss = criterion(outputs, targets)
                    loss.backward()
                    optimizer.step()

                # Log training loss
                avg_loss += loss.item()

            # Calculate average loss
            avg_loss /= len(train_loader)

        avg_loss /= num_splits

        if avg_loss < best_avg_loss:
            best_avg_loss = avg_loss
            best_lr = lr

    return best_lr

def main(data_file, learning_rates):
    best_lr = train_with_cross_validation(data_file, learning_rates)
    print("Best learning rate:", best_lr)

if __name__ == "__main__":
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Hyperparameter tuning with cross-validation.')

    # Add arguments
    parser.add_argument('data_file', type=str, help='File path for data')
    parser.add_argument('--learning_rates', nargs='+', type=float, help='List of learning rates to try')

    # Parse the arguments
    args = parser.parse_args()

    # Access the parsed arguments
    data_file = args.data_file
    learning_rates = args.learning_rates

    main(data_file, learning_rates)
