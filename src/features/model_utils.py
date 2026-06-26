from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFECV
from sklearn.svm import SVR
from sklearn.feature_selection import VarianceThreshold

from typing import Any
import sys
import importlib
sys.path.append('../') 
from features import general_func as gf
importlib.reload(gf)

def make_feature_pipeline(method: str, k:int):
    
    match method:
        case "all_features":
            return Pipeline([
                ("scaler", StandardScaler())
            ])
        
        case "SelectKBest":
            return Pipeline([
                ("scaler", StandardScaler()),
                ("select", SelectKBest(score_func=f_regression, k=k))
            ])
        
        case "RFECV":
            estimator = SVR(kernel="linear")
            return RFECV(estimator, step=1, cv=k)
        
        case "VarianceThreshold":
            return Pipeline([
                ("var", VarianceThreshold()),
                ("scaler", StandardScaler())
            ])
        
        case "PCA":
            return Pipeline([
                ("scaler", StandardScaler()),
                ("select", PCA(n_components=k))
            ])
        
        case _:
            gf.fail(msg= "Unkown feature pipeline", error="ValueError")

    
def make_model_pipeline(feature_pipeline: Pipeline, model: Any):
    return Pipeline([
        ("features", feature_pipeline),
        ("model", model)
    ])