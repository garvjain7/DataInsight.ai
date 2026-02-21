import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, mean_squared_error

# Load data
df = pd.read_csv("../data/processed/cleaned_superstore.csv")

# Feature selection
X = df.drop(columns=["sales"])
Y = df["sales"]

# Split
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

# Scale
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# -------- Detect Problem Type --------
if Y.nunique() > 20:
    problem_type = "regression"
    config = {
        "units": 1,
        "activation": "linear",
        "loss": "mse",
        "metric": "mae"
    }
else:
    problem_type = "classification"
    config = {
        "units": Y.nunique(),
        "activation": "softmax",
        "loss": "sparse_categorical_crossentropy",
        "metric": "accuracy"
    }

print(f"[INFO] Problem type: {problem_type.upper()}")

# -------- Build Model --------
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(config["units"], activation=config["activation"])
])

# Compile
model.compile(
    optimizer="adam",
    loss=config["loss"],
    metrics=[config["metric"]]
)

# Train
history = model.fit(
    X_train,
    Y_train,
    validation_data=(X_test, Y_test),
    epochs=20,
    batch_size=32
)

# Evaluate
evaluation = model.evaluate(X_test, Y_test)
print("Final Evaluation:", evaluation)

# -------- Capture Loss --------
final_training_loss = history.history["loss"][-1]
final_validation_loss = history.history["val_loss"][-1]

print("\n📉 Final Training Loss:", final_training_loss)
print("📉 Final Validation Loss:", final_validation_loss)

# -------- Final Evaluation Metrics --------
predictions = model.predict(X_test)

if problem_type == "regression":
    rmse = np.sqrt(mean_squared_error(Y_test, predictions))
    print("\n📊 Final Evaluation Metrics:")
    print("MAE:", history.history["mae"][-1])
    print("RMSE:", rmse)

else:
    predicted_classes = np.argmax(predictions, axis=1)
    cm = confusion_matrix(Y_test, predicted_classes)

    print("\n📊 Final Evaluation Metrics:")
    print("Accuracy:", history.history["accuracy"][-1])
    print("Confusion Matrix:\n", cm)