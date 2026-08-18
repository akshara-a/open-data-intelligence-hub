from src.data_preprocessing import preprocess_data
from src.logistic_model import run_logistic_model
from src.decision_tree_model import run_decision_tree
from src.random_forest_model import run_random_forest


def main():

    print("=" * 50)
    print("TASK 9 - PURCHASE PREDICTION")
    print("=" * 50)

    df, X_train, X_test, y_train, y_test = preprocess_data(
        "data/customerData_500k.csv"
    )

    print("\nRunning Logistic Regression...")
    run_logistic_model(
        X_train,
        X_test,
        y_train,
        y_test
    )

    print("\nRunning Decision Tree...")
    run_decision_tree(
        X_train,
        X_test,
        y_train,
        y_test
    )

    print("\nRunning Random Forest...")
    run_random_forest(
        X_train,
        X_test,
        y_train,
        y_test
    )

    print("\nTask 9 completed successfully!")


if __name__ == "__main__":
    main()