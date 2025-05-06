from .base_metric import BaseMetric
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class R2MatrixRunnerMetric(BaseMetric):
    use_normalized = True
    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        return pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y)

    def score(self, x: pd.Series, y: pd.Series) -> float:
        try:
            df = pd.DataFrame({'x': x, 'y': y}).dropna()
            if df.shape[0] < 2:
                return np.nan

            model = LinearRegression()
            model.fit(df[['x']], df['y'])
            r2 = model.score(df[['x']], df['y'])
            return float(r2)

        except Exception as e:
            print(f"[R2MatrixRunnerMetric] Error: {e}")
            return np.nan
