import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_histograms(dataset):
    num_features = dataset.shape[1]

    # Create a figure and axis objects
    fig, axs = plt.subplots(num_features, 1, figsize=(8, 12), sharex=True)  # Adjust figsize as needed

    # Iterate through each feature and plot its histogram
    for i in range(num_features):
        axs[i].hist(dataset[:, i], bins=20)  # Adjust the number of bins as needed
        axs[i].set_title(f"Feature {i}")
        axs[i].set_xlabel('Value')
        axs[i].set_ylabel('Frequency')

    plt.tight_layout()
    
    # Set same x-axis scale for all subplots
    plt.xlim(dataset.min().min(), dataset.max().max())  # Sets the x-axis limits to the min and max values in the entire dataset

    plt.show()

# Example usage
if __name__ == "__main__":
    # Load your dataset
    # Replace 'your_dataset.csv' with the actual path to your dataset
    # dataset = pd.read_csv('your_dataset.csv')
    # # Extract feature names and data
    # feature_names = df.columns.values
    # dataset = df.values
    
    dataset = np.random.randn(1000, 6)  # Generating random data, replace with your dataset
    dataset[:, 4] += 1
    
    # Plot feature statistics
    plot_histograms(dataset)
