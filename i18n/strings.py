LANGS = ["FR","EN","ES","IT","ZH"]

STRINGS = {
    "brand": {
        "FR": "SmartRisk Pro — Notation Crédit",
        "EN": "SmartRisk Pro — Credit Scoring",
        "ES": "SmartRisk Pro — Calificación de Crédito",
        "IT": "SmartRisk Pro — Valutazione del Credito",
        "ZH": "SmartRisk Pro — 信用评分",
    },
    "subtitle": {
        "FR": "Scoring en temps réel • Explications • Tableau de bord • Seuil orienté profit • Multilingue",
        "EN": "Real-time scoring • Explainability • Dashboard • Profit-oriented threshold • Multilingual",
        "ES": "Scoring en tiempo real • Explicabilidad • Tablero • Umbral orientado al beneficio • Multilingüe",
        "IT": "Scoring in tempo reale • Spiegabilità • Dashboard • Soglia orientata al profitto • Multilingue",
        "ZH": "实时评分 • 可解释性 • 仪表盘 • 利润阈值 • 多语言",
    },
    "home_eda": {
        "FR": "Explorer les distributions, corrélations et valeurs manquantes du dataset.",
        "EN": "Explore distributions, correlations and missing values of the dataset.",
        "ES": "Explora distribuciones, correlaciones y valores faltantes del conjunto de datos.",
        "IT": "Esplora distribuzioni, correlazioni e valori mancanti del dataset.",
        "ZH": "探索数据集的分布、相关性和缺失值。",
    },
    "home_score": {
        "FR": "Scorer un individu, obtenir la probabilité de défaut et l’explication des facteurs clés.",
        "EN": "Score an individual, get default probability and key-factor explanations.",
        "ES": "Califica a un individuo, obtén la probabilidad de incumplimiento y explicaciones de factores clave.",
        "IT": "Valuta un individuo, ottieni la probabilità di default e le spiegazioni dei fattori chiave.",
        "ZH": "对个体评分，获得违约概率和关键因素解释。",
    },
    "author": {
        "FR": "Projet réalisé par Ivan NFINDA",
        "EN": "Project by Ivan NFINDA",
        "ES": "Proyecto de Ivan NFINDA",
        "IT": "Progetto di Ivan NFINDA",
        "ZH": "项目作者 Ivan NFINDA",
    },
}

def tr(key: str, lang: str) -> str:
    lang = lang if lang in LANGS else "EN"
    return STRINGS.get(key, {}).get(lang, STRINGS.get(key, {}).get("EN",""))
