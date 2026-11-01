from sklearn.linear_model import Ridge

def train_regression(X_train, y_train):
    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)
    return model
