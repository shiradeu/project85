from .base_metric import BaseMetric
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

class TTestRunnerMetric(BaseMetric):
    use_normalized = False 
    
    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        return pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y)

    def score(self, x: pd.Series, y: pd.Series) -> float:
        try:
            df = pd.DataFrame({'x': x, 'y': y}).dropna()
            if df.shape[0] < 10:
                return np.nan

            median_y = df['y'].median()
            group1 = df[df['y'] >= median_y]['x']
            group2 = df[df['y'] < median_y]['x']

            if len(group1) < 2 or len(group2) < 2:
                return np.nan

            stat, p_value = ttest_ind(group1, group2, nan_policy='omit')
            return 1 - p_value  

        except Exception as e:
            print(f"[TTestRunnerMetric] Error: {e}")
            return np.nan
