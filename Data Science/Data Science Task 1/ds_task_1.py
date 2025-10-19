import os
import zipfile
import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


def load_dataset(zip_path: str):
    """Extract Titanic-Dataset.csv from the zip and return as DataFrame."""
    # Convert to absolute path to avoid VSCode relative path issues
    zip_path = os.path.abspath(zip_path)

    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"Archive not found: {zip_path}")

    with zipfile.ZipFile(zip_path, 'r') as z:
        csv_files = [f for f in z.namelist() if f.endswith(".csv")]

        if not csv_files:
            raise FileNotFoundError("No CSV files found inside the provided archive.")

        # Since your archive has Titanic-Dataset.csv, use it
        dataset_name = csv_files[0]
        print(f"Using dataset: {dataset_name}")

        with z.open(dataset_name) as f:
            df = pd.read_csv(f)

    return df


def build_pipeline(numeric_features, categorical_features, model):
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features)
        ]
    )

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", model)
    ])
    return pipeline


def main(zip_path, output_dir):
    df = load_dataset(zip_path)

    if "Survived" not in df.columns:
        raise ValueError("Dataset does not contain 'Survived' column. Cannot train model.")

    X = df.drop("Survived", axis=1)
    y = df["Survived"]

    numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_features = X.select_dtypes(include=["object", "category"]).columns.tolist()

    # Split data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define models
    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42)
    }

    results = {}

    for name, model in models.items():
        print(f"\nTraining {name}...")
        pipeline = build_pipeline(numeric_features, categorical_features, model)
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_val)
        acc = accuracy_score(y_val, preds)
        cv_acc = cross_val_score(pipeline, X, y, cv=3, scoring="accuracy").mean()
        print(f"Validation Accuracy: {acc:.4f}, Cross-Validation Accuracy: {cv_acc:.4f}")
        print(classification_report(y_val, preds))
        results[name] = (acc, pipeline)

    # Choose best model
    best_model_name = max(results, key=lambda k: results[k][0])
    best_pipeline = results[best_model_name][1]
    print(f"\nBest model selected: {best_model_name}")

    # Save predictions
    preds = best_pipeline.predict(X)
    out_path = os.path.abspath(os.path.join(output_dir, "titanic_predictions.csv"))
    pd.DataFrame({"PassengerId": df.index, "Survived_Pred": preds}).to_csv(out_path, index=False)
    print(f"Predictions saved to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
    "--zip", 
    type=str, 
    default=r"C:\Users\sudsm\Desktop\CodeSoft\CodeSoft Code\Data Science\Data Science Task 1\archive.zip", 
    help="Path to zip file containing Titanic dataset"
)

    parser.add_argument("--out", type=str, default=".", help="Output directory")
    args = parser.parse_args()

    main(args.zip, args.out)
