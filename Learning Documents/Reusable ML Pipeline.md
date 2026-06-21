# Learning Material 1: What is a Reusable ML Pipeline?

## 1. Simple Meaning

A **reusable ML pipeline** is a structured machine learning workflow that can be run again and again without rewriting the entire code.

It connects all important ML steps in one organized flow:

```text
Raw Data → Cleaning → Feature Engineering → Model Training → Evaluation → Prediction
```

Instead of writing separate, unorganized code for each step, we create a pipeline where each step is clearly defined and reusable.

---

## 2. Why Do We Need a Reusable ML Pipeline?

In real-world ML projects, data may change often.

For example, in a customer churn project, every month the company may get new customer data. If the ML code is not reusable, the developer has to clean, prepare, train, and test the model manually every time.

A reusable pipeline solves this problem.

It allows us to:

| Benefit                    | Explanation                                                 |
| -------------------------- | ----------------------------------------------------------- |
| Save Time                  | Same code can be reused for new data                        |
| Reduce Errors              | Less manual work means fewer mistakes                       |
| Improve Consistency        | Same steps are followed every time                          |
| Make Code Clean            | Each step has a clear responsibility                        |
| Support Production Use     | The pipeline can be used in real applications               |
| Improve Team Collaboration | Other developers can understand and run the workflow easily |

---

## 3. Example Without a Reusable Pipeline

This is an example of scattered code:

```python
df["Age"] = df["Age"].fillna(df["Age"].median())
df["Gender"] = df["Gender"].fillna("Unknown")
df["ContractType"] = df["ContractType"].map({"Monthly": 0, "Yearly": 1})
model.fit(X_train, y_train)
```

This approach may work for small practice tasks, but it becomes difficult to maintain when the project grows.

Problems:

```text
- Cleaning logic is mixed with training logic
- Code is difficult to reuse
- Same steps may need to be copied again
- Hard to debug
- Hard to move into production
```

---

## 4. Example With a Reusable ML Pipeline

A reusable pipeline organizes the process:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline(steps=[
    ("missing_value_handler", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("model", LogisticRegression())
])

pipeline.fit(X_train, y_train)
```

Here, the pipeline does three things in order:

| Step               | Purpose                 |
| ------------------ | ----------------------- |
| SimpleImputer      | Handles missing values  |
| StandardScaler     | Scales numerical values |
| LogisticRegression | Trains the ML model     |

Once created, the same pipeline can be used for training and prediction.

---

## 5. Real-Life Example: Customer Churn Prediction

For a subscription business, we may want to predict whether a customer will leave the service.

The pipeline may look like this:

```text
Customer Data
     ↓
Remove duplicate records
     ↓
Handle missing values
     ↓
Convert categorical values into numbers
     ↓
Create useful churn-related features
     ↓
Train ML model
     ↓
Evaluate model performance
     ↓
Predict churn risk for new customers
```

---

## 6. Components of a Reusable ML Pipeline

| Component           | Meaning                                                  |
| ------------------- | -------------------------------------------------------- |
| Data Loading        | Reading data from CSV, Excel, database, or API           |
| Data Validation     | Checking whether required columns and values are present |
| Data Cleaning       | Handling missing values, duplicates, and invalid data    |
| Feature Engineering | Creating useful new columns from existing data           |
| Encoding            | Converting text categories into numeric values           |
| Scaling             | Bringing numeric values to a common scale                |
| Model Training      | Training the machine learning algorithm                  |
| Model Evaluation    | Checking how well the model performs                     |
| Prediction          | Using the model on new unseen data                       |
| Documentation       | Explaining why each step was used                        |

---

## 7. Simple Analogy

Think of a reusable ML pipeline like a factory assembly line.

In a factory:

```text
Raw material → Cleaning → Processing → Packaging → Final Product
```

In ML:

```text
Raw data → Cleaning → Feature Engineering → Model Training → Prediction
```

Each step has a fixed responsibility. If new data comes in, it goes through the same process automatically.

---

## 8. Why It Is Important in ML Engineering

ML engineering is not only about building a model once. It is about building a system that can be repeated, improved, and maintained.

A reusable ML pipeline helps students move from basic machine learning to real-world ML engineering.

It teaches them how to write ML code that is:

```text
- Organized
- Repeatable
- Testable
- Explainable
- Production-ready
```

---

## 9. Key Difference: Normal ML Code vs Reusable ML Pipeline

| Normal ML Code               | Reusable ML Pipeline         |
| ---------------------------- | ---------------------------- |
| Steps are written separately | Steps are connected in order |
| Difficult to reuse           | Easy to reuse                |
| More chance of mistakes      | Less chance of mistakes      |
| Hard to maintain             | Easy to maintain             |
| Good for practice            | Good for real projects       |
| Not production-friendly      | Production-friendly          |

---

## 10. Student Takeaway

By the end of this learning material, students should understand that a reusable ML pipeline is a structured way to build ML projects.

It helps convert raw business data into predictions through a clean, repeatable, and well-documented process.

For the customer churn mini project, the reusable ML pipeline will help students build a complete workflow that can clean customer data, prepare features, train a churn prediction model, evaluate the result, and make predictions on new customers.
