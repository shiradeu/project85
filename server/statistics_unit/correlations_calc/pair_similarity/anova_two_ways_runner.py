from .base_metric import BaseMetric
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

class TwoWayAnovaRunnerMetric(BaseMetric):
    use_normalized: bool = False  # לא מנרמלים ב־ANOVA

    def is_applicable(self, x: pd.Series, y: pd.DataFrame) -> bool:
        try:
            return (
                pd.api.types.is_numeric_dtype(x) and
                isinstance(y, pd.DataFrame) and
                y.shape[1] == 2 and
                all(pd.api.types.is_categorical_dtype(y[col]) or y[col].dtype == object for col in y.columns)
            )
        except:
            return False

    def score(self, x: pd.Series, y: pd.DataFrame) -> float:
        try:
            df = pd.DataFrame({
                "dependent": x,
                "factor1": y.iloc[:, 0],
                "factor2": y.iloc[:, 1]
            }).dropna()

            formula = "dependent ~ C(factor1) + C(factor2) + C(factor1):C(factor2)"
            model = smf.ols(formula, data=df).fit()
            anova_table = smf.stats.anova_lm(model, typ=2)
            min_p = anova_table["PR(>F)"].min()

            return 1 - min_p  # יותר גבוה = קשר חזק יותר
        except Exception as e:
            print(f"[TwoWayAnovaRunnerMetric] Error: {e}")
            return np.nan
