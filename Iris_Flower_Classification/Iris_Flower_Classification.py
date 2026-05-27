# Iris Flower Classification using Machine Learning

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load Iris Dataset
iris = load_iris()

# Create DataFrame
df = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
)

# Add target column
df['species'] = iris.target

print("Dataset Preview:")
print(df.head())

# Input Features
X = iris.data

# Output Labels
y = iris.target

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create Model
model = LogisticRegression(max_iter=200)

# Train Model
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:", accuracy * 100, "%")

# User Input
print("\nEnter Flower Details:")

sepal_length = float(input("Sepal Length: "))
sepal_width = float(input("Sepal Width: "))
petal_length = float(input("Petal Length: "))
petal_width = float(input("Petal Width: "))

# Prediction
result = model.predict([[
    sepal_length,
    sepal_width,
    petal_length,
    petal_width
]])

# Flower Names
flower_names = iris.target_names

print("\nPredicted Flower Species:",
      flower_names[result][0])

# Simple Graph
plt.scatter(
    df['sepal length (cm)'],
    df['petal length (cm)']
)

plt.xlabel("Sepal Length")
plt.ylabel("Petal Length")
plt.title("Iris Dataset Visualization")

plt.show()