import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

df = pd.read_csv("data/Titanic-Dataset.csv")

print("Dataset Loaded Successfully")
print(df.head())
required_columns = [
    "Pclass",
    "Sex",
    "Age",
    "SibSp",
    "Parch",
    "Fare",
    "Embarked",
    "Survived"
]

missing_columns = []

for column in required_columns:
    if column not in df.columns:
        missing_columns.append(column)

if len(missing_columns) > 0:
    raise ValueError(f"Missing Columns : {missing_columns}")

print("Data Validation Completed")

X = df.drop("Survived", axis=1)

# Keeping only useful features
X = X[
    [
        "Pclass",
        "Sex",
        "Age",
        "SibSp",
        "Parch",
        "Fare",
        "Embarked",
    ]
]

y = df["Survived"]

numerical_features = [
    "Age",
    "Fare",
    "SibSp",
    "Parch",
    "Pclass"
]

categorical_features = [
    "Sex",
    "Embarked"
]

numerical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        ),
        (
            "scaler",
            StandardScaler()
        ),
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(handle_unknown="ignore")
        ),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            numerical_pipeline,
            numerical_features
        ),
        (
            "cat",
            categorical_pipeline,
            categorical_features
        ),
    ]
)


pipeline = Pipeline(
    steps=[
        (
            "preprocessing",
            preprocessor
        ),
        (
            "model",
            RandomForestClassifier(
                n_estimators=100,
                random_state=42
            )
        ),
    ]
)

print("Pipeline Created Successfully")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

pipeline.fit(X_train, y_train)

print("Model Training Completed")

predictions = pipeline.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\nAccuracy : ", accuracy)

print("\nClassification Report\n")

print(
    classification_report(
        y_test,
        predictions
    )
)

new_passenger = pd.DataFrame(
    {
        "Pclass": [1],
        "Sex": ["female"],
        "Age": [30],
        "SibSp": [0],
        "Parch": [0],
        "Fare": [80],
        "Embarked": ["C"],
    }
)

prediction = pipeline.predict(new_passenger)

print("\nPrediction")

if prediction[0] == 1:
    print("Passenger is likely to Survive")
else:
    print("Passenger is NOT likely to Survive")