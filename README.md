# SmartRisk Pro — Credit Scoring (Streamlit)
**By Ivan NFINDA** · Multilingual (FR/EN/ES/IT/ZH) · Kaggle dataset (*Give Me Some Credit*) · Real-time scoring · Batch · Metrics · SHAP · Macro FX API · OECD.

## Demo rapide
```bash
pip install -r requirements.txt
python src/train.py          # entraîne LightGBM + CV, sauvegarde models/pipeline.joblib
streamlit run app.py         # lance l'app
