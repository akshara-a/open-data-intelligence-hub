from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

def get_baseline_pipelines(preprocessor, random_state=42):
    """
    Constructs Scikit-Learn pipelines combining preprocessing with baseline classification algorithms.
    """
    pipelines = {
        "Logistic Regression": Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", LogisticRegression(max_iter=1000, random_state=random_state))
            ]
        ),
        "Decision Tree": Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", DecisionTreeClassifier(random_state=random_state))
            ]
        ),
        "Random Forest": Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", RandomForestClassifier(random_state=random_state))
            ]
        ),
        "Gradient Boosting": Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", GradientBoostingClassifier(random_state=random_state))
            ]
        )
    }
    return pipelines

def train_models(pipelines, X_train, y_train):
    """
    Fits all baseline models on the training dataset.
    """
    trained_models = {}
    for name, pipeline in pipelines.items():
        print(f"[Model Training] Fitting baseline {name}...")
        pipeline.fit(X_train, y_train)
        trained_models[name] = pipeline
    return trained_models
