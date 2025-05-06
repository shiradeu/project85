from .base_metric import BaseMetric
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

class ChiSquarePValueRunnerMetric(BaseMetric):
    use_normalized: bool = False  # על משתנים קטגוריים אין טעם לנרמל

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

            # צריך לפחות שני ערכים בכל משתנה
            if contingency.shape[0] < 2 or contingency.shape[1] < 2:
                return np.nan

            chi2, p_value, _, _ = chi2_contingency(contingency)

            # הופכים את p-value לציון בין 0 ל־1: ככל שיותר קטן - הקשר חזק יותר
            return 1 - p_value
        except Exception as e:
            print(f"[ChiSquarePValueRunnerMetric] Error: {e}")
            return np.nan
