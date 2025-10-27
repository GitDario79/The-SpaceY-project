import joblib, numpy as np
from sklearn.linear_model import LogisticRegression

def main():
    # tiny binary dataset with 3 features
    X = np.array([
        [0.1, 0.2, 0.3],
        [1.0, 0.9, 0.8],
        [0.2, 0.1, 0.4],
        [0.9, 1.1, 0.7],
        [0.3, 0.2, 0.6],
        [0.8, 0.9, 1.0],
    ])
    y = np.array([0, 1, 0, 1, 0, 1])

    clf = LogisticRegression(max_iter=500)
    clf.fit(X, y)
    joblib.dump(clf, "models/model.joblib")
    print("Saved models/model.joblib")

if __name__ == "__main__":
    main()
