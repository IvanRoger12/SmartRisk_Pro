import os, joblib, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from lightgbm import LGBMClassifier

RAW = "data/raw/cs-training.csv"
MODEL = "models/pipeline.joblib"
BASELINE = "models/baseline_sample.parquet"  # échantillon de référence pour le PSI

def main():
    if not os.path.exists(RAW):
        raise FileNotFoundError(f"Missing data file: {RAW}")
    df = pd.read_csv(RAW)
    y = df["SeriousDlqin2yrs"].astype(int)
    X = df.drop(columns=["SeriousDlqin2yrs"])

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    pipe = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("clf", LGBMClassifier(
            n_estimators=500, learning_rate=0.05,
            subsample=0.9, colsample_bytree=0.9,
            max_depth=-1, random_state=42
        ))
    ])

    pipe.fit(Xtr, ytr)
    proba = pipe.predict_proba(Xte)[:,1]
    auc = roc_auc_score(yte, proba)
    print("AUC valid:", round(auc,4))

    os.makedirs(os.path.dirname(MODEL), exist_ok=True)
    joblib.dump(pipe, MODEL)
    print("Saved →", MODEL)

    # baseline PSI (sample 20k max) — je stocke seulement les features numériques
    base = X.select_dtypes(include=["number"]).sample(min(20000, len(X)), random_state=42)
    base.to_parquet(BASELINE, index=False)
    print("Saved PSI baseline →", BASELINE)

if __name__ == "__main__":
    main()
