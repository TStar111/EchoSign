import torch
import torch.nn as nn
import pandas as pd
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset
from torch.optim import Adam
import argparse
import wandb

from models_NN import SimpleNN


def create_and_train_nn_classification(csv_file, model_save_path, wandb_project_name):
    # Initialize wandb
    wandb.init(project=wandb_project_name)

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

    # Step 6: Instantiate your neural network
    input_dim = X_train.shape[1]
    hidden_dim = 64
    output_dim = len(pd.unique(y))  # Number of unique classes in your target variable
    model = SimpleNN(input_dim, hidden_dim, output_dim)

    # Step 7: Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=0.001)

    # Step 8: Train your neural network
    num_epochs = 30
    for epoch in range(num_epochs):
        for inputs, targets in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            
        # Log training loss to wandb
        wandb.log({"Training Loss": loss.item(), "Epoch": epoch + 1})

        # Testing
        model.eval()
        with torch.no_grad():
            test_outputs = model(X_test_tensor)
            test_loss = criterion(test_outputs, y_test_tensor)
            _, predicted = torch.max(test_outputs, 1)
            correct = (predicted == y_test_tensor).sum().item()
            accuracy = correct / len(y_test_tensor)

        # Log testing loss and accuracy to wandb
        wandb.log({"Test Loss": test_loss.item(), "Test Accuracy": accuracy, "Epoch": epoch + 1})

    # Step 9: Save your trained model
    torch.save(model.state_dict(), model_save_path)
    print("Model has been saved successfully!")

def main(data_file, model_file, wandb_project_name):
    create_and_train_nn_classification(data_file, model_file, wandb_project_name)

if __name__ == "__main__":
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Process two strings.')

    # Add two string arguments
    parser.add_argument('data_file', type=str, help='File path for data')
    parser.add_argument('model_file', type=str, help='File path for where model will be uploaded')
    parser.add_argument('wandb_project_name', type=str, help='Wandb project name')

    # Parse the arguments
    args = parser.parse_args()

    # Access the parsed arguments
    data_file = args.data_file
    model_file = args.model_file
    wandb_project_name = args.wandb_project_name

    main(data_file, model_file, wandb_project_name)

# Command
# python train_NN_model.py ../../data/dataset_single/dataset_single_none.csv ../../models/initial_none.pt echosign_single


# TODO: Consider other achitectures beyond simple NN