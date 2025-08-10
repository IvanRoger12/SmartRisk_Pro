from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, auc

def compute_metrics(y_true, y_proba):
    fpr, tpr, thr = roc_curve(y_true, y_proba)
    auc_roc = roc_auc_score(y_true, y_proba)
    prec, rec, thr2 = precision_recall_curve(y_true, y_proba)
    pr_auc = auc(rec, prec)
    return {"roc_auc": auc_roc, "fpr": fpr, "tpr": tpr, "thr": thr, "pr_auc": pr_auc, "prec": prec, "rec": rec}
