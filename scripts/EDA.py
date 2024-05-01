import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_histograms(dataset1, dataset2):
    num_features = 5

    # Create a figure and axis objects
    fig, axs = plt.subplots(num_features, 2, figsize=(8, 12), sharex=True)  # Adjust figsize as needed

    # Iterate through each feature and plot its histogram
    for i in range(num_features):
        axs[i, 0].hist(dataset1[:, i], bins=20)  # Adjust the number of bins as needed
        axs[i, 0].set_title(f"Feature {i}")
        axs[i, 0].set_xlabel('Value')
        axs[i, 0].set_ylabel('Frequency')

        axs[i, 0].hist(dataset1[:, i+14], bins=20)  # Adjust the number of bins as needed
        # axs[i, 0].set_title(f"Feature {i+14}")
        axs[i, 0].set_xlabel('Value')
        axs[i, 0].set_ylabel('Frequency')

    # Iterate through each feature and plot its histogram
    for i in range(num_features):
        axs[i, 1].hist(dataset2[:, i], bins=20)  # Adjust the number of bins as needed
        axs[i, 1].set_title(f"Feature {i}")
        axs[i, 1].set_xlabel('Value')
        axs[i, 1].set_ylabel('Frequency')

        axs[i, 1].hist(dataset2[:, i+14], bins=20)  # Adjust the number of bins as needed
        # axs[i, 1].set_title(f"Feature {i+14}")
        axs[i, 1].set_xlabel('Value')
        axs[i, 1].set_ylabel('Frequency')

    # # Iterate through each feature and plot its histogram
    # for i in range(num_features):
    #     axs[i, 2].hist(dataset3[:, i], bins=20)  # Adjust the number of bins as needed
    #     axs[i, 2].set_title(f"Feature {i}")
    #     axs[i, 2].set_xlabel('Value')
    #     axs[i, 2].set_ylabel('Frequency')

    #     axs[i, 2].hist(dataset3[:, i+14], bins=20)  # Adjust the number of bins as needed
    #     axs[i, 2].set_title(f"Feature {i+14}")
    #     axs[i, 2].set_xlabel('Value')
    #     axs[i, 2].set_ylabel('Frequency')

    plt.tight_layout()
    
    # Set same x-axis scale for all subplots
    # plt.xlim(dataset1[:, 0:5].min().min(), dataset1.max().max())  # Sets the x-axis limits to the min and max values in the entire dataset

    plt.show()

# Example usage
if __name__ == "__main__":
    # Load your dataset
    # Replace 'your_dataset.csv' with the actual path to your dataset
    df1 = pd.read_csv('data/data_pcb/ricky-none2.csv')
    feature_names1 = df1.columns.values
    dataset1 = df1.values

    df2 = pd.read_csv('data/data_pcb/ria-none.csv')
    feature_names2 = df2.columns.values
    dataset2 = df2.values

    # df3 = pd.read_csv('data/dataset_double_word/somya-but.csv')
    # feature_names3 = df3.columns.values
    # dataset3 = df3.values
    
    # dataset = np.random.randn(1000, 6)  # Generating random data, replace with your dataset
    # dataset[:, 4] += 1
    
    # Plot feature statistics
    plot_histograms(dataset1, dataset2)
