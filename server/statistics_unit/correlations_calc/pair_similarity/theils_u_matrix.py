from .base_metric import BaseMetric
import pandas as pd
import numpy as np
from math import log2

class TheilsUMatrixMetric(BaseMetric):
    use_normalized = False  
    
    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        return (x.dtype == "object" or pd.api.types.is_categorical_dtype(x)) and \
               (y.dtype == "object" or pd.api.types.is_categorical_dtype(y))

    def conditional_entropy(self, x, y):
        y_counter = y.value_counts()
        xy_counter = pd.crosstab(x, y)
        total = len(x)
        entropy = 0.0
        for xi in xy_counter.index:
            for yj in xy_counter.columns:
                p_xy = xy_counter.loc[xi, yj] / total
                p_y = y_counter[yj] / total
                if p_xy > 0:
                    entropy += p_xy * log2(p_y / p_xy)
        return entropy

    def score(self, x: pd.Series, y: pd.Series) -> float:
        try:
            x = x.astype(str)
            y = y.astype(str)

            h_x = self.conditional_entropy(x, x)
            h_x_given_y = self.conditional_entropy(x, y)

            if h_x == 0:
                return 0.0
            else:
                return (h_x - h_x_given_y) / h_x

        except Exception as e:
            print(f"[TheilsUMatrixMetric] Error: {e}")
            return np.nan