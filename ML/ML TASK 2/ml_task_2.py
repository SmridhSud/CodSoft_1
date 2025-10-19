# ml_task_2.py
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score


# Paths to dataset
TRAIN_PATH = r"C:\Users\sudsm\Desktop\CodeSoft\CodeSoft Code\ML\ML TASK 2\fraudTrain.csv"
TEST_PATH = r"C:\Users\sudsm\Desktop\CodeSoft\CodeSoft Code\ML\ML TASK 2\fraudTest.csv"


def load_data():
    print("Loading datasets...")
    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)
    df = pd.concat([train_df, test_df], ignore_index=True)
    print(f"Dataset shape: {df.shape}")
    return df


def preprocess_data(df):
    print("Preprocessing data...")

    # Drop transaction ID and datetime if present
    drop_cols = ["Unnamed: 0", "trans_date_trans_time", "trans_num"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # Target variable
    y = df["is_fraud"]
    X = df.drop(columns=["is_fraud"])

    # Identify categorical columns
    cat_cols = X.select_dtypes(include=["object"]).columns
    print("Categorical columns detected:", list(cat_cols))

    # Label encode high-cardinality categorical columns, one-hot encode small ones
    le = LabelEncoder()
    for col in cat_cols:
        if X[col].nunique() > 20:   # treat as high-cardinality
            X[col] = le.fit_transform(X[col])
        else:
            dummies = pd.get_dummies(X[col], prefix=col, drop_first=True)
            X = pd.concat([X.drop(columns=[col]), dummies], axis=1)

    # Normalize numerical features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)


def train_and_evaluate(X_train, X_test, y_train, y_test):
    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42),
        "DecisionTree": DecisionTreeClassifier(class_weight="balanced", random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
    }

    best_model, best_score = None, 0

    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        print(f"{name} acc={acc:.4f} f1={f1:.4f}")
        print(classification_report(y_test, y_pred))

        if f1 > best_score:
            best_score = f1
            best_model = name

    print(f"\nBest model: {best_model} with F1={best_score:.4f}")


def main():
    assert Path(TRAIN_PATH).exists(), f"{TRAIN_PATH} not found."
    assert Path(TEST_PATH).exists(), f"{TEST_PATH} not found."

    df = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(df)
    train_and_evaluate(X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    main()
