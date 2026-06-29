import joblib
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from data_loader import load_data
from preprocessing import preprocess_data
from feature_engineering import feature_engineering

df = load_data("data/customer_churn.csv")
df = preprocess_data(df)
df = feature_engineering(df)

if 'customerID' in df.columns:
    df = df.drop('customerID', axis=1)

X = df.drop('Churn', axis=1)
y = df['Churn']

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = joblib.load("models/churn_model.pkl")

pred = model.predict(X_test)

print("Accuracy:")
print(accuracy_score(y_test, pred))

print("\nClassification Report:")
print(classification_report(y_test, pred))