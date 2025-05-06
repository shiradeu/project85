from .base_metric import BaseMetric
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

class RandomForestRunnerMetric(BaseMetric):
    use_normalized = True  
    
    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        return pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y)

    def score(self, x: pd.Series, y: pd.Series) -> float:
        try:
            df = pd.DataFrame({'x': x, 'y': y}).dropna()
            if df.shape[0] < 5: 
                return np.nan

            model = RandomForestRegressor(n_estimators=100, random_state=0)
            model.fit(df[['x']], df['y'])
            score = model.score(df[['x']], df['y'])  # R²
            return float(score)

        except Exception as e:
            print(f"[RandomForestRunnerMetric] Error: {e}")
            return np.nan
