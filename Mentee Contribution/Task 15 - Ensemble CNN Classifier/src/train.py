from src.data_loader import load_mnist_data
from src.cnn_models import create_cnn_model_1
from src.preprocessing import normalize_images


def train_single_cnn():
    print("Loading MNIST dataset...")

    x_train, y_train, x_test, y_test = (
        load_mnist_data()
    )

    x_train, x_test = normalize_images(
        x_train,
        x_test
    )

    print("Creating CNN model...")

    model = create_cnn_model_1()

    print("Training CNN model...")

    model.fit(
        x_train,
        y_train,
        epochs=3,
        batch_size=64,
        validation_split=0.1
    )

    print("Evaluating CNN model...")

    loss, accuracy = model.evaluate(
        x_test,
        y_test,
        verbose=0
    )

    print("Single CNN accuracy:", accuracy)

    model.save(
        "models/single_cnn_model.keras"
    )

    print("Single CNN model saved successfully.")


if __name__ == "__main__":
    train_single_cnn()