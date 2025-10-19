# train_movie_genre.py
import zipfile, pickle, shutil, os
from pathlib import Path
import re
import textwrap
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report, f1_score
import argparse

# CONFIG
ARCHIVE = ARCHIVE = r"C:\Users\sudsm\Desktop\CodeSoft\CodeSoft Code\ML\archive.zip"
FILE_IN_ZIP = "Genre Classification Dataset/train_data.txt"
OUTPUT_DIR = Path("movie_genre_classifier_out")
TOP_N = 12            # set None to keep all
SAMPLES_PER_CLASS = 400   # set None to use all (lower to speed up)
TEST_SIZE = 0.18
RANDOM_STATE = 42
TFIDF_MAX_FEATURES = 8000

def parse_file(content):
    lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
    lines = [ln for ln in lines if not ln.lower().startswith("id :::")]
    recs = []
    for ln in lines:
        parts = [p.strip() for p in ln.split(" ::: ")]
        if len(parts) >= 4:
            recs.append({"id": parts[0], "title": parts[1], "genre": parts[2].lower().strip(), "description": " ::: ".join(parts[3:])})
    return pd.DataFrame(recs)

def main():
    assert Path(ARCHIVE).exists(), f"{ARCHIVE} not found."
    with zipfile.ZipFile(ARCHIVE, 'r') as z:
        raw = z.read(FILE_IN_ZIP).decode('utf-8', errors='replace')
    df = parse_file(raw)
    df = df.dropna(subset=['description', 'genre']).copy()
    df['description'] = df['description'].astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

    if TOP_N:
        top = df['genre'].value_counts().nlargest(TOP_N).index.tolist()
        df = df[df['genre'].isin(top)].copy()
        print("Keeping top genres:", top)

    if SAMPLES_PER_CLASS:
        df = df.groupby('genre').apply(lambda g: g.sample(n=min(len(g), SAMPLES_PER_CLASS), random_state=RANDOM_STATE)).reset_index(drop=True)

    X = df['description'].values
    y = df['genre'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE)

    pipelines = {
        "LogisticRegression": Pipeline([('tfidf', TfidfVectorizer(max_features=TFIDF_MAX_FEATURES, ngram_range=(1,2), stop_words='english')), ('clf', LogisticRegression(max_iter=1500, solver='liblinear'))]),
        "MultinomialNB": Pipeline([('tfidf', TfidfVectorizer(max_features=TFIDF_MAX_FEATURES, ngram_range=(1,2), stop_words='english')), ('clf', MultinomialNB())]),
        "LinearSVC": Pipeline([('tfidf', TfidfVectorizer(max_features=TFIDF_MAX_FEATURES, ngram_range=(1,2), stop_words='english')), ('clf', LinearSVC(max_iter=20000))])
    }

    results = {}
    for name, pipe in pipelines.items():
        print("Training", name)
        pipe.fit(X_train, y_train)
        preds = pipe.predict(X_test)
        acc = accuracy_score(y_test, preds)
        macro_f1 = f1_score(y_test, preds, average='macro')
        print(f"{name} acc={acc:.4f} macro_f1={macro_f1:.4f}")
        print(classification_report(y_test, preds, zero_division=0))
        results[name] = (pipe, acc, macro_f1)

    best_name = max(results.keys(), key=lambda k: results[k][1])
    best_pipe = results[best_name][0]
    print("Best model:", best_name)

    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "best_model.pkl", "wb") as f:
        pickle.dump({"pipeline": best_pipe}, f)

    (OUTPUT_DIR / "README.txt").write_text(textwrap.dedent(f"""
    Best model: {best_name}
    TF-IDF max features: {TFIDF_MAX_FEATURES}
    Top genres kept: {TOP_N}
    Samples per class: {SAMPLES_PER_CLASS}
    """).strip())

    # zip it
    zipname = OUTPUT_DIR.parent / (OUTPUT_DIR.name + ".zip")
    if zipname.exists(): zipname.unlink()
    shutil.make_archive(str(OUTPUT_DIR.parent / OUTPUT_DIR.name), 'zip', root_dir=str(OUTPUT_DIR))
    print("Saved outputs to:", OUTPUT_DIR, "zipped at:", zipname)

if __name__ == "__main__":
    main()
