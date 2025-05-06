from .base_metric import BaseMetric
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

class CramersVMatrixRunnerMetric(BaseMetric):
    use_normalized = False  
    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        try:
            return (
                (pd.api.types.is_categorical_dtype(x) or x.dtype == object) and
                (pd.api.types.is_categorical_dtype(y) or y.dtype == object)
            )
        except:
            return False

    def score(self, x: pd.Series, y: pd.Series) -> float:
        try:
            contingency = pd.crosstab(x, y)
            if contingency.shape[0] < 2 or contingency.shape[1] < 2:
                return np.nan

            chi2, _, _, _ = chi2_contingency(contingency)
            n = contingency.sum().sum()
            r, k = contingency.shape
            denom = n * (min(k, r) - 1)
            if denom == 0:
                return np.nan

            cramers_v = np.sqrt(chi2 / denom)
            return cramers_v
        except Exception as e:
            print(f"[CramersVMatrixRunnerMetric] Error: {e}")
            return np.nan
