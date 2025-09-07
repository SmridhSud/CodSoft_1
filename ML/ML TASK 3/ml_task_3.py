import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score

# Load dataset
data = pd.read_csv(r"C:\Users\sudsm\Desktop\CodeSoft\CodeSoft Code\ML\ML TASK 3\Churn_Modelling.csv")

print("Dataset Shape:", data.shape)
print(data.head())

# Drop irrelevant columns
X = data.drop(["RowNumber", "CustomerId", "Surname", "Exited"], axis=1)
y = data["Exited"]

# Encode categorical variables
le = LabelEncoder()
X["Geography"] = le.fit_transform(X["Geography"])
X["Gender"] = le.fit_transform(X["Gender"])

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# Define models
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, random_state=42)
}

best_model, best_f1 = None, 0

# Train & Evaluate
for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"{name} -> Accuracy: {acc:.4f}, F1 Score: {f1:.4f}")
    print(classification_report(y_test, y_pred))

    if f1 > best_f1:
        best_f1 = f1
        best_model = name

print(f"\nBest Model: {best_model} with F1 Score = {best_f1:.4f}")
