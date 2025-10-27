def predict_proba(features):
    base = 0.3
    bump = min(len(features) * 0.02, 0.4)
    return round(base + bump, 3)
