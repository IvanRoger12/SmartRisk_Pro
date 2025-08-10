# i18n dictionary — Author: Ivan NFINDA
LANGS = ["FR","EN","ES","IT","ZH"]

T = {
    "brand":{"FR":"SmartRisk Pro — Scoring Crédit","EN":"SmartRisk Pro — Credit Scoring","ES":"SmartRisk Pro — Puntaje de Crédito","IT":"SmartRisk Pro — Punteggio di Credito","ZH":"SmartRisk Pro — 信用评分"},
    "subtitle":{"FR":"Scoring en temps réel • Explications • Dashboard • Batch • Multilingue","EN":"Real-time scoring • Explanations • Dashboard • Batch • Multilingual","ES":"Scoring en tiempo real • Explicaciones • Panel • Lote • Multilingüe","IT":"Scoring in tempo reale • Spiegazioni • Dashboard • Batch • Multilingue","ZH":"实时评分 • 可解释性 • 仪表盘 • 批量 • 多语言"},
    "author":{"FR":"Projet réalisé par Ivan NFINDA","EN":"Project by Ivan NFINDA","ES":"Proyecto de Ivan NFINDA","IT":"Progetto di Ivan NFINDA","ZH":"项目作者：Ivan NFINDA"},
    "nav_home":{"FR":"Accueil","EN":"Home","ES":"Inicio","IT":"Home","ZH":"首页"},
    "nav_eda":{"FR":"Analyse exploratoire","EN":"Exploratory Analysis","ES":"Análisis exploratorio","IT":"Analisi esplorativa","ZH":"探索性分析"},
    "nav_score":{"FR":"Scoring individuel","EN":"Individual Scoring","ES":"Scoring individual","IT":"Punteggio individuale","ZH":"单个评分"},
    "nav_batch":{"FR":"Scoring batch","EN":"Batch Scoring","ES":"Scoring por lotes","IT":"Punteggio in batch","ZH":"批量评分"},
    "nav_metrics":{"FR":"Métriques & Explications","EN":"Metrics & Explanations","ES":"Métricas y Explicaciones","IT":"Metriche e Spiegazioni","ZH":"指标与解释"},
    "nav_macro":{"FR":"Contexte macro (FX/API)","EN":"Macro context (FX/API)","ES":"Contexto macro (FX/API)","IT":"Contesto macro (FX/API)","ZH":"宏观环境 (汇率/API)"},
    "nav_oecd":{"FR":"Indicateurs OCDE","EN":"OECD Indicators","ES":"Indicadores OCDE","IT":"Indicatori OCSE","ZH":"经合组织指标"},
    "lang_label":{"FR":"Langue","EN":"Language","ES":"Idioma","IT":"Lingua","ZH":"语言"},
    "score":{"FR":"Score (0–100)","EN":"Score (0–100)","ES":"Puntuación (0–100)","IT":"Punteggio (0–100)","ZH":"评分 (0–100)"},
    "defprob":{"FR":"Probabilité de défaut","EN":"Default probability","ES":"Probabilidad de impago","IT":"Probabilità di default","ZH":"违约概率"},
    "reco":{"FR":"Recommandations","EN":"Recommendations","ES":"Recomendaciones","IT":"Raccomandazioni","ZH":"建议"},
    "healthy":{"FR":"Profil sain","EN":"Healthy profile","ES":"Perfil sano","IT":"Profilo sano","ZH":"较健康的档案"},
    "upload":{"FR":"Importer un CSV clients","EN":"Upload clients CSV","ES":"Cargar CSV de clientes","IT":"Carica CSV clienti","ZH":"上传客户CSV"},
    "download":{"FR":"Télécharger les prédictions","EN":"Download predictions","ES":"Descargar predicciones","IT":"Scarica previsioni","ZH":"下载预测结果"},
    "needs_model":{"FR":"Modèle introuvable. Entraînez-le (src/train.py).","EN":"Model not found. Train it first (src/train.py).","ES":"Modelo no encontrado. Entrénelo primero (src/train.py).","IT":"Modello non trovato. Esegui il training (src/train.py).","ZH":"未找到模型。请先训练 (src/train.py)。"},
    "val_csv":{"FR":"Jeu de validation (avec colonne SeriousDlqin2yrs)","EN":"Validation CSV (with SeriousDlqin2yrs column)","ES":"CSV de validación (con columna SeriousDlqin2yrs)","IT":"CSV di validazione (con colonna SeriousDlqin2yrs)","ZH":"验证CSV（包含SeriousDlqin2yrs列）"},
    "oecd_intro":{"FR":"Charge un CSV OCDE local ou colle une URL CSV de l’API OCDE.","EN":"Load a local OECD CSV or paste a CSV URL from the OECD API.","ES":"Carga un CSV local de la OCDE o pega una URL CSV de la API de la OCDE.","IT":"Carica un CSV OCSE locale o incolla un URL CSV dell'API OCSE.","ZH":"加载本地经合组织CSV或粘贴经合组织API的CSV链接。"},
    "oecd_local":{"FR":"Fichier CSV local","EN":"Local CSV file","ES":"Archivo CSV local","IT":"File CSV locale","ZH":"本地CSV文件"},
    "oecd_url":{"FR":"URL CSV (API OCDE)","EN":"CSV URL (OECD API)","ES":"URL CSV (API OCDE)","IT":"URL CSV (API OCSE)","ZH":"CSV链接（经合组织API）"},
    "oecd_parse":{"FR":"Colonnes (auto-détectées, modifiables)","EN":"Columns (auto-detected, editable)","ES":"Columnas (auto-detectadas, editables)","IT":"Colonne (auto-rilevate, modificabili)","ZH":"列（自动检测，可编辑）"},
    "time_col":{"FR":"Colonne temps","EN":"Time column","ES":"Columna de tiempo","IT":"Colonna del tempo","ZH":"时间列"},
    "value_col":{"FR":"Colonne valeur","EN":"Value column","ES":"Columna de valor","IT":"Colonna valore","ZH":"数值列"},
    "country_col":{"FR":"Colonne pays","EN":"Country column","ES":"Columna país","IT":"Colonna paese","ZH":"国家列"},
    "indic_col":{"FR":"Colonne indicateur (optionnel)","EN":"Indicator column (optional)","ES":"Columna indicador (opcional)","IT":"Colonna indicatore (opzionale)","ZH":"指标列（可选）"},
    "filters":{"FR":"Filtres","EN":"Filters","ES":"Filtros","IT":"Filtri","ZH":"筛选"},
    "download_csv":{"FR":"Télécharger les données filtrées","EN":"Download filtered data","ES":"Descargar datos filtrados","IT":"Scarica dati filtrati","ZH":"下载筛选数据"}
}
def tr(key, lang): return T.get(key, {}).get(lang, T.get(key, {}).get("EN", key))
