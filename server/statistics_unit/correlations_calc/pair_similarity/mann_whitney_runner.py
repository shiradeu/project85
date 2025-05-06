from .base_metric import BaseMetric
import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu

class MannWhitneyRunnerMetric(BaseMetric):
    use_normalized = False  
    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        try:
            return pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y)
        except:
            return False

    def score(self, x: pd.Series, y: pd.Series) -> float:
        try:
            median = y.median()
            group1 = x[y >= median]
            group2 = x[y < median]

            if len(group1) < 2 or len(group2) < 2:
                return np.nan

            _, p_value = mannwhitneyu(group1, group2, alternative='two-sided')
            return 1 - p_value  
        except Exception as e:
            print(f"[MannWhitneyRunnerMetric] Error: {e}")
            return np.nan
