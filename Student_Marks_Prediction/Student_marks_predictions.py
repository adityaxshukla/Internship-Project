# Student Marks Prediction using Machine Learning

# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Sample Dataset
data = {
    'Hours': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Marks': [15, 20, 32, 38, 45, 55, 60, 70, 80, 90]
}

# Convert into DataFrame
df = pd.DataFrame(data)

print("Dataset:")
print(df)

# Input (Hours) and Output (Marks)
X = df[['Hours']]
y = df['Marks']

# Split dataset into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create model
model = LinearRegression()

# Train model
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

print("\nPredicted Marks:")
print(predictions)

# User Input
hours = float(input("\nEnter study hours: "))

predicted_marks = model.predict([[hours]])

print(f"Predicted Marks for {hours} study hours = {predicted_marks[0]:.2f}")

# Graph
plt.scatter(X, y, color='blue', label='Actual Data')
plt.plot(X, model.predict(X), color='red', label='Regression Line')

plt.title("Student Marks Prediction")
plt.xlabel("Study Hours")
plt.ylabel("Marks")
plt.legend()

plt.show()