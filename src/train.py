import os, joblib, pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from lightgbm import LGBMClassifier
import numpy as np

RAW = "data/raw/cs-training.csv"
MODEL = "models/pipeline.joblib"

def train_cv(X, y, n_splits=5, seed=42):
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    oof = np.zeros(len(y))
    models = []
    for fold, (tr, va) in enumerate(skf.split(X, y), 1):
        Xtr, Xva = X.iloc[tr], X.iloc[va]
        ytr, yva = y.iloc[tr], y.iloc[va]
        pipe = Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("clf", LGBMClassifier(
                n_estimators=600, learning_rate=0.03,
                subsample=0.9, colsample_bytree=0.9,
                max_depth=-1, num_leaves=31,
                random_state=seed+fold, n_jobs=-1
            ))
        ])
        pipe.fit(Xtr, ytr)
        proba = pipe.predict_proba(Xva)[:,1]
        oof[va] = proba
        auc = roc_auc_score(yva, proba)
        print(f"Fold {fold}: AUC={auc:.4f}")
        models.append(pipe)
    print("OOF AUC:", roc_auc_score(y, oof))
    # on garde le dernier modèle (ou on peut en empiler un, mais ici simple)
    return models[-1]

def main():
    if not os.path.exists(RAW):
        raise FileNotFoundError(f"Missing data file: {RAW}")
    df = pd.read_csv(RAW)
    y = df["SeriousDlqin2yrs"].astype(int)
    X = df.drop(columns=["SeriousDlqin2yrs"])
    os.makedirs("models", exist_ok=True)
    model = train_cv(X, y)
    joblib.dump(model, MODEL)
    print("Saved →", MODEL)

if __name__ == "__main__":
    main()
