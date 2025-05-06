from .base_metric import BaseMetric
import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_regression

class MutualInfoRunnerMetric(BaseMetric):
    use_normalized = False  
    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        return pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y)

    def score(self, x: pd.Series, y: pd.Series) -> float:
        try:
            x = x.values.reshape(-1, 1)
            y = y.values
            mi = mutual_info_regression(x, y, discrete_features=False, random_state=0)
            return float(mi[0])
        except Exception as e:
            print(f"[MutualInfoRunnerMetric] Error: {e}")
            return np.nan
