import numpy as np
from sklearn.feature_selection import mutual_info_regression
from .base_group_metric import BaseGroupMetric

class MutualInfoGroupMetric(BaseGroupMetric):
    def is_applicable(self, X, y) -> bool:
        return all(np.issubdtype(dtype, np.number) for dtype in X.dtypes) and np.issubdtype(y.dtype, np.number)

    def score(self, X, y) -> float:
        try:
            score = mutual_info_regression(X, y, discrete_features=False, random_state=0)
            return float(np.mean(score))
        except:
            return np.nan