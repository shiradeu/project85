from .base_metric import BaseMetric
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

class ChiSquareRunnerMetric(BaseMetric):
    use_normalized: bool = False  # על משתנים קטגוריים לא מנרמלים

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

            # חייבים לפחות שתי קטגוריות בכל ציר
            if contingency.shape[0] < 2 or contingency.shape[1] < 2:
                return np.nan

            chi2, _, _, _ = chi2_contingency(contingency)
            return chi2
        except Exception as e:
            print(f"[ChiSquareRunnerMetric] Error: {e}")
            return np.nan
