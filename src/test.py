import mlflow
import mlflow.sklearn

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

# -------------------------
# Data
# -------------------------
X, y = load_diabetes(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------
# MLflow setup
# -------------------------
mlflow.set_experiment("basic_mlflow_test")

# -------------------------
# Experiment run
# -------------------------
with mlflow.start_run(run_name="ridge_test"):

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("model", Ridge(alpha=1.0))
    ])

    # Cross-validation
    scores = cross_validate(
        pipe,
        X_train,
        y_train,
        cv=5,
        scoring={
            "r2": "r2",
            "mae": "neg_mean_absolute_error",
            "rmse": "neg_root_mean_squared_error"
        }
    )

    # Metrics
    r2 = scores["test_r2"].mean()
    mae = -scores["test_mae"].mean()
    rmse = -scores["test_rmse"].mean()

    print("R2:", r2)
    print("MAE:", mae)
    print("RMSE:", rmse)

    # Log parameters
    mlflow.log_param("model", "Ridge")
    mlflow.log_param("alpha", 1.0)

    # Log metrics
    mlflow.log_metric("r2", r2)
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("rmse", rmse)

    # Log model
    mlflow.sklearn.log_model(pipe, "model")