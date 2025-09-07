import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import re

# --- 1. Data Loading and Initial Inspection ---

# Load the dataset with a specified encoding
file_path = r"C:\Users\sudsm\Desktop\CodeSoft\CodeSoft Code\Data Science\Data Science Task 2\IMDb Movies India.csv"
encodings = ['utf-8', 'ISO-8859-1', 'Windows-1252', 'utf-16']
df = None

# Try different encodings to load the dataset
for enc in encodings:
    try:
        df = pd.read_csv(file_path, encoding=enc)
        print(f"Dataset loaded successfully with encoding: {enc}")
        break  # Exit the loop if successful
    except UnicodeDecodeError:
        print(f"Failed to decode with encoding: {enc}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please ensure the path is correct.")
        exit()

# Display initial data info
print("\n--- Initial Data Info ---")
df.info()
print("\n--- First 5 Rows ---")
print(df.head())
print("\n--- Missing Values Before Preprocessing ---")
print(df.isnull().sum())

# --- 2. Data Preprocessing and Feature Engineering ---

# Rename columns for easier access
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
df.rename(columns={'actor_1': 'actor1', 'actor_2': 'actor2', 'actor_3': 'actor3'}, inplace=True)

# Convert 'year' to numeric, handling non-numeric values
df['year'] = pd.to_numeric(df['year'], errors='coerce')

# Check for NaN values in 'year' after conversion
if df['year'].isnull().all():
    print("All values in 'year' are NaN after conversion. Please check the data.")
    exit()

# Fill missing values with the mode if it exists
year_mode = df['year'].mode()
if not year_mode.empty:
    df['year'].fillna(year_mode[0], inplace=True)
else:
    print("No mode found for 'year'.")
    exit()

df['year'] = df['year'].astype(int)  # Convert to integer after filling NaN

# Clean 'duration' column and convert to minutes (numeric)
def clean_duration(duration_str):
    if isinstance(duration_str, str):
        match = re.search(r'(\d+)\s*min', duration_str)
        if match:
            return int(match.group(1))
    return np.nan  # Return NaN for non-string or unmatchable values

df['duration_minutes'] = df['duration'].apply(clean_duration)
df['duration_minutes'].fillna(df['duration_minutes'].median(), inplace=True)

# Clean 'rating' column and convert to numeric
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['rating'].fillna(df['rating'].median(), inplace=True)

# Clean 'votes' column and convert to numeric
def clean_votes(votes_str):
    if isinstance(votes_str, str):
        return int(votes_str.replace(',', ''))
    return np.nan

df['votes_numeric'] = df['votes'].apply(clean_votes)
df['votes_numeric'].fillna(df['votes_numeric'].median(), inplace=True)

# Handle 'genre' - Multi-label binarization
df['genre'] = df['genre'].astype(str).apply(lambda x: [g.strip() for g in x.split(',') if g.strip()])
mlb_genre = MultiLabelBinarizer()
genre_encoded = mlb_genre.fit_transform(df['genre'])
genre_df = pd.DataFrame(genre_encoded, columns=mlb_genre.classes_)
df = pd.concat([df, genre_df], axis=1)

# Handle 'director' and 'actors' - Label Encoding
le_director = LabelEncoder()
df['director_encoded'] = le_director.fit_transform(df['director'].astype(str))

# Actor encoding
le_actor1 = LabelEncoder()
le_actor2 = LabelEncoder()
le_actor3 = LabelEncoder()

df['actor1_encoded'] = le_actor1.fit_transform(df['actor1'].astype(str))
df['actor2_encoded'] = le_actor2.fit_transform(df['actor2'].astype(str))
df['actor3_encoded'] = le_actor3.fit_transform(df['actor3'].astype(str))

# Drop original columns that have been processed or are not needed
columns_to_drop = ['name', 'duration', 'genre', 'director', 'actor1', 'actor2', 'actor3', 'votes', 'all_actors']
df.drop(columns=columns_to_drop, errors='ignore', inplace=True)

print("\n--- Missing Values After Preprocessing ---")
print(df.isnull().sum())
print("\n--- Data Info After Preprocessing ---")
df.info()
print("\n--- First 5 Rows After Preprocessing ---")
print(df.head())

# --- 3. Feature Selection and Data Splitting ---

# Define features (X) and target (y)
X = df.drop(columns=['rating'])  # 'rating' is our target
y = df['rating']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\nTraining features shape: {X_train.shape}")
print(f"Testing features shape: {X_test.shape}")
print(f"Training target shape: {y_train.shape}")
print(f"Testing target shape: {y_test.shape}")

# --- 4. Model Training ---

# Initialize and train various regression models
models = {
    'Linear Regression': LinearRegression(),
    'Ridge Regression': Ridge(random_state=42),
    'Lasso Regression': Lasso(random_state=42),
    'Decision Tree Regressor': DecisionTreeRegressor(random_state=42),
    'Random Forest Regressor': RandomForestRegressor(n_estimators=100, random_state=42),
    'Gradient Boosting Regressor': GradientBoostingRegressor(n_estimators=100, random_state=42)
}

results = {}

print("\n--- Model Training and Evaluation ---")
for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    results[name] = {'MSE': mse, 'R2': r2}

    print(f"{name} - Mean Squared Error: {mse:.4f}")
    print(f"{name} - R^2 Score: {r2:.4f}")

# --- 5. Model Comparison and Selection ---

print("\n--- Model Comparison ---")
for name, metrics in results.items():
    print(f"{name}: MSE={metrics['MSE']:.4f}, R2={metrics['R2']:.4f}")

# Select the best model based on R2 score (or MSE)
best_model_name = max(results, key=lambda k: results[k]['R2'])
best_model = models[best_model_name]
print(f"\nBest performing model: {best_model_name} (R2: {results[best_model_name]['R2']:.4f})")

# --- 6. Cross-Validation for Robustness (Optional but Recommended) ---

print(f"\n--- Cross-Validation for {best_model_name} ---")
kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(best_model, X, y, cv=kf, scoring='r2')

print(f"Cross-validation R^2 scores: {cv_scores}")
print(f"Mean CV R^2: {np.mean(cv_scores):.4f} (+/- {np.std(cv_scores):.4f})")

# --- 7. Feature Importance (for tree-based models) ---

if hasattr(best_model, 'feature_importances_'):
    print(f"\n--- Feature Importances for {best_model_name} ---")
    feature_importances = pd.Series(best_model.feature_importances_, index=X.columns)
    print(feature_importances.sort_values(ascending=False).head(10))

    plt.figure(figsize=(10, 6))
    feature_importances.sort_values(ascending=False).head(10).plot(kind='bar')
    plt.title('Top 10 Feature Importances')
    plt.ylabel('Importance')
    plt.tight_layout()
    plt.show()

# --- 8. Prediction on New Data (Example) ---

print("\n--- Example Prediction on New Data ---")

# Create a sample new movie data point
# Note: The new data must have the same columns as X_train after preprocessing
# and encoding. This is a simplified example. In a real application, you'd
# need to apply the same preprocessing steps and encoders used during training.

# For demonstration, let's create a dummy row similar to X_train structure
# This assumes you know the encoded values for new director/actors/genres.
# In a real scenario, you'd use the fitted LabelEncoders and MultiLabelBinarizer.

# Example: A new movie 'The Great Adventure'
# Genre: Action, Adventure
# Director: 'Christopher Nolan' (if in training data, else 'Other' or new encoding)
# Actor1: 'Leonardo DiCaprio', Actor2: 'Tom Hardy', Actor3: 'Joseph Gordon-Levitt'

# To make a realistic prediction, we need to reverse the preprocessing for a new input.
# This is complex for a single example without a full pipeline for new data.
# Instead, let's predict for an existing row from the test set to show functionality.

# Let's pick the first row from the original test set (before dropping columns)
original_test_row = df.iloc[X_test.index[0]]
actual_rating = original_test_row['rating']
new_movie_features = X_test.iloc[[0]]  # Get the features for this row

predicted_rating_example = best_model.predict(new_movie_features)[0]

print(f"Actual Rating for a sample movie: {actual_rating:.2f}")
print(f"Predicted Rating for the same sample movie: {predicted_rating_example:.2f}")
print(f"Difference: {abs(actual_rating - predicted_rating_example):.2f}")

# --- 9. Residual Plot (Optional) ---
plt.figure(figsize=(10, 6))
sns.residplot(x=y_test, y=y_pred, lowess=True, color='green')
plt.xlabel("Actual Ratings")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.grid(True)
plt.show()
