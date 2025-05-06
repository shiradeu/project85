from .base_metric import BaseMetric
import pandas as pd
import numpy as np

class CorrelationRunnerMetric(BaseMetric):
    use_normalized = True

    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        return pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y)

    def score(self, x: pd.Series, y: pd.Series) -> float:
        try:
            return x.corr(y)
        except:
            return np.nan