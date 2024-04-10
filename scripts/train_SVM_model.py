import argparse
import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def train_svm(csv_file, model_path):
    # Load data from CSV file
    data = pd.read_csv(csv_file)

    # Assuming the last column is the target label and rest are features
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train SVM model
    clf = svm.SVC()
    clf.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = clf.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

    # Save the trained model to disk
    joblib.dump(clf, model_path)
    print("Model saved at:", model_path)

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Train SVM model and save it')
    parser.add_argument('data_file', type=str, help='Path to CSV file containing data')
    parser.add_argument('model_path', type=str, help='Path where trained model will be saved')
    args = parser.parse_args()

    # Train SVM model and save it
    train_svm(args.data_file, args.model_path)

# To run this:
# python train_SVM_model.py ../data/dataset_double/dataset_double.csv ../models/double_SVM.pkl
