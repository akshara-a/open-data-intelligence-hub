print("THIS IS MY MAIN FILE")
from src.data_loader import load_data
from src.preprocess import split_features_target, split_train_test

# Load dataset
file_path = "data/customer_churn.csv"
data = load_data(file_path)

# Split Features and Target
X, y = split_features_target(data)
print("Number of features:", len(X.columns))
print(X.columns)
print(data.head())
print("\nColumns:")
print(list(data.columns))
print("\nData Types:")
print(data.dtypes)


# Split into Training and Testing
X_train, X_test, y_train, y_test = split_train_test(X, y)

print("Training Data Shape:")
print(X_train.shape)

print("\nTesting Data Shape:")
print(X_test.shape)

print("\nTraining Target Shape:")
print(y_train.shape)

print("\nTesting Target Shape:")
print(y_test.shape)
from sklearn.linear_model import LogisticRegression

# Create model
model = LogisticRegression(max_iter=1000)

# Train model
model.fit(X_train, y_train)

print("Model trained successfully!")
# Make predictions
y_pred = model.predict(X_test)

print("Predictions completed!")
from sklearn.metrics import accuracy_score, classification_report

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(5,4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

plt.show()
from sklearn.metrics import roc_curve, roc_auc_score

# Get prediction probabilities
y_prob = model.predict_proba(X_test)[:, 1]

# Calculate ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_prob)

# Calculate AUC score
auc = roc_auc_score(y_test, y_prob)

# Plot ROC curve
plt.figure(figsize=(6,5))
plt.plot(fpr, tpr, label=f"AUC = {auc:.2f}")
plt.plot([0, 1], [0, 1], 'k--')

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend(loc="lower right")

plt.show()

print("AUC Score:", auc)
import joblib

joblib.dump(model, "models/customer_churn_model.pkl")
# Save feature names
joblib.dump(X.columns.tolist(), "models/feature_names.pkl")

print("Feature names saved successfully!")

print("Model saved successfully!")