LANGS = ["FR","EN","ES","IT","ZH"]

T = {
  "brand": {
    "FR":"SmartRisk Pro — Notation Crédit",
    "EN":"SmartRisk Pro — Credit Scoring",
    "ES":"SmartRisk Pro — Puntaje de Crédito",
    "IT":"SmartRisk Pro — Punteggio di Credito",
    "ZH":"SmartRisk Pro — 信用评分",
  },
  "subtitle":{
    "FR":"Scoring en temps réel • Explications • Tableau de bord • Batch • Multilingue",
    "EN":"Real-time scoring • Explanations • Dashboard • Batch • Multilingual",
    "ES":"Scoring en tiempo real • Explicaciones • Panel • Lote • Multilingüe",
    "IT":"Scoring in tempo reale • Spiegazioni • Dashboard • Batch • Multilingue",
    "ZH":"实时评分 • 可解释性 • 仪表盘 • 批量 • 多语言",
  },
  "author":{
    "FR":"Projet réalisé par Ivan NFINDA",
    "EN":"Project by Ivan NFINDA",
    "ES":"Proyecto de Ivan NFINDA",
    "IT":"Progetto di Ivan NFINDA",
    "ZH":"项目作者：Ivan NFINDA",
  },
  "cta_start":{"FR":"Démarrer","EN":"Get started","ES":"Empezar","IT":"Inizia","ZH":"开始"},
  "nav_home":{"FR":"Accueil","EN":"Home","ES":"Inicio","IT":"Home","ZH":"首页"},
  "nav_eda":{"FR":"Analyse exploratoire","EN":"Exploratory Analysis","ES":"Análisis exploratorio","IT":"Analisi esplorativa","ZH":"探索性分析"},
  "nav_score":{"FR":"Scoring individuel","EN":"Individual Scoring","ES":"Scoring individual","IT":"Punteggio individuale","ZH":"单个评分"},
  "nav_batch":{"FR":"Scoring batch","EN":"Batch Scoring","ES":"Scoring por lotes","IT":"Punteggio in batch","ZH":"批量评分"},
  "nav_metrics":{"FR":"Métriques & Explications","EN":"Metrics & Explanations","ES":"Métricas y Explicaciones","IT":"Metriche e Spiegazioni","ZH":"指标与解释"},
  "nav_macro":{"FR":"Contexte macro (FX/API)","EN":"Macro context (FX/API)","ES":"Contexto macro (FX/API)","IT":"Contesto macro (FX/API)","ZH":"宏观环境 (汇率/API)"},
  "score":{"FR":"Score (0–100)","EN":"Score (0–100)","ES":"Puntuación (0–100)","IT":"Punteggio (0–100)","ZH":"评分 (0–100)"},
  "defprob":{"FR":"Probabilité de défaut","EN":"Default probability","ES":"Probabilidad de impago","IT":"Probabilità di default","ZH":"违约概率"},
  "reco":{"FR":"Recommandations","EN":"Recommendations","ES":"Recomendaciones","IT":"Raccomandazioni","ZH":"建议"},
  "healthy":{"FR":"Profil sain","EN":"Healthy profile","IT":"Profilo sano","ES":"Perfil sano","ZH":"较健康的档案"},
  "upload":{"FR":"Importer un CSV clients","EN":"Upload clients CSV","ES":"Cargar CSV de clientes","IT":"Carica CSV clienti","ZH":"上传客户CSV"},
  "download":{"FR":"Télécharger les prédictions","EN":"Download predictions","ES":"Descargar predicciones","IT":"Scarica predizioni","ZH":"下载预测结果"},
  "needs_model":{"FR":"Modèle introuvable. Entraînez-le (src/train.py).","EN":"Model not found. Train it first (src/train.py).","ES":"Modelo no encontrado. Entrénelo primero (src/train.py).","IT":"Modello non trovato. Esegui il training (src/train.py).","ZH":"未找到模型。请先训练 (src/train.py)。"},
  "val_csv":{"FR":"Jeu de validation (avec colonne SeriousDlqin2yrs)","EN":"Validation CSV (with SeriousDlqin2yrs column)","ES":"CSV de validación (con columna SeriousDlqin2yrs)","IT":"CSV di validazione (con colonna SeriousDlqin2yrs)","ZH":"验证CSV（包含SeriousDlqin2yrs列）"},
  "home_eda":{
    "FR":"Explorez le dataset, valeurs manquantes, distributions, corrélations.",
    "EN":"Explore dataset, missing values, distributions, correlations.",
    "ES":"Explore el conjunto, valores faltantes, distribuciones, correlaciones.",
    "IT":"Esplora il dataset, valori mancanti, distribuzioni, correlazioni.",
    "ZH":"探索数据集、缺失率、分布与相关性。"
  },
  "home_score":{
    "FR":"Score 0–100, PD, jauge, conseils et scénario What-if.",
    "EN":"Score 0–100, PD, gauge, tips and What-if scenario.",
    "ES":"Puntaje 0–100, PD, indicador, consejos y What-if.",
    "IT":"Punteggio 0–100, PD, gauge, consigli e What-if.",
    "ZH":"分数、违约概率、仪表盘及假设情景。"
  }
}
def tr(key, lang):
    return T.get(key, {}).get(lang, T.get(key, {}).get("EN", key))
