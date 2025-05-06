from .base_metric import BaseMetric
import pandas as pd
import numpy as np
from scipy.stats import f_oneway

class AnovaRunnerMetric(BaseMetric):
    use_normalized: bool = False  # לא מנרמלים ANOVA – הוא בודק הבדלים בין קבוצות

    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        try:
            return (
                pd.api.types.is_numeric_dtype(x) and
                (pd.api.types.is_categorical_dtype(y) or y.dtype == object)
            )
        except:
            return False

    def score(self, x: pd.Series, y: pd.Series) -> float:
        try:
            groups = [x[y == category] for category in y.dropna().unique()]
            if len(groups) < 2:
                return np.nan  # צריך לפחות שתי קבוצות
            stat, p_value = f_oneway(*groups)
            return 1 - p_value  # הופכים את המובהקות לציון (כמו יתר המדדים: יותר גבוה = קשר חזק)
        except Exception as e:
            print(f"[AnovaRunnerMetric] Error: {e}")
            return np.nan
