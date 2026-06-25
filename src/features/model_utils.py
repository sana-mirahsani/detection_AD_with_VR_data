from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

def make_feature_pipeline(method):
    
    if method == "all":
        return StandardScaler()

    elif method == "k50":
        return Pipeline([
            ("scaler", StandardScaler()),
            ("select", SelectKBest(score_func=f_regression, k=50))
        ])

    elif method == "k20":
        return Pipeline([
            ("scaler", StandardScaler()),
            ("select", SelectKBest(score_func=f_regression, k=20))
        ])

    elif method == "pca":
        return Pipeline([
            ("scaler", StandardScaler()),
            ("pca", PCA(n_components=10))
        ])
    
def make_model_pipeline(feature_pipeline, model):
    return Pipeline([
        ("features", feature_pipeline),
        ("model", model)
    ])