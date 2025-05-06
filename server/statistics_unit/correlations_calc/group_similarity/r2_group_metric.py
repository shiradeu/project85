import numpy as np
from sklearn.linear_model import LinearRegression
from .base_group_metric import BaseGroupMetric

class R2GroupMetric(BaseGroupMetric):
    def is_applicable(self, X, y) -> bool:
        return all(np.issubdtype(dtype, np.number) for dtype in X.dtypes) and np.issubdtype(y.dtype, np.number)

    def score(self, X, y) -> float:
        try:
            model = LinearRegression().fit(X, y)
            return model.score(X, y)
        except:
            return np.nan