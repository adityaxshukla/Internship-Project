# Email Spam Detection using Machine Learning

# Import libraries
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Sample Dataset
data = {
    'EmailText': [
        'Congratulations! You won a free lottery ticket',
        'Get free recharge now',
        'Hello Aditya, how are you?',
        'Meeting at 5 PM today',
        'Win cash prizes instantly',
        'Your account has been updated',
        'Claim your free gift card now',
        'Project submission deadline tomorrow'
    ],

    'Label': [
        'Spam',
        'Spam',
        'Ham',
        'Ham',
        'Spam',
        'Ham',
        'Spam',
        'Ham'
    ]
}

# Convert into DataFrame
df = pd.DataFrame(data)

print("Dataset:")
print(df)

# Input and Output
X = df['EmailText']
y = df['Label']

# Convert text into numerical data
vectorizer = CountVectorizer()

X_vectorized = vectorizer.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)

# Create Model
model = MultinomialNB()

# Train Model
model.fit(X_train, y_train)

# Prediction
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:", accuracy * 100, "%")

# User Input
email = input("\nEnter Email Message: ")

# Transform input
email_vector = vectorizer.transform([email])

# Predict
result = model.predict(email_vector)

print("\nPrediction:", result[0])