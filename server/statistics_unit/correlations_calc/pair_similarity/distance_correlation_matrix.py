from .base_metric import BaseMetric
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform

class DistanceCorrelationMatrixMetric(BaseMetric):
    use_normalized = True  

    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        try:
            return pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y)
        except:
            return False

    def score(self, x: pd.Series, y: pd.Series) -> float:
        def distance_covariance(a, b):
            A = squareform(pdist(a[:, None]))
            B = squareform(pdist(b[:, None]))
            A_mean = A.mean(axis=0, keepdims=True)
            B_mean = B.mean(axis=0, keepdims=True)
            A_centered = A - A_mean - A_mean.T + A.mean()
            B_centered = B - B_mean - B_mean.T + B.mean()
            return np.sqrt(np.mean(A_centered * B_centered))

        try:
            x_vals = x.values
            y_vals = y.values

            dcov = distance_covariance(x_vals, y_vals)
            dvar_x = distance_covariance(x_vals, x_vals)
            dvar_y = distance_covariance(y_vals, y_vals)

            if dvar_x > 0 and dvar_y > 0:
                return dcov / np.sqrt(dvar_x * dvar_y)
            else:
                return 0.0
        except Exception as e:
            print(f"[DistanceCorrelationMatrixMetric] Error: {e}")
            return np.nan
