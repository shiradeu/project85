from .base_metric import BaseMetric
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class PcaRunnerMetric(BaseMetric):
    use_normalized = True 
    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        return pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y)

    def score(self, x: pd.Series, y: pd.Series) -> float:
        try:
            df_pair = pd.DataFrame({'x': x, 'y': y}).dropna()
            if df_pair.shape[0] < 2:
                return np.nan

            scaler = StandardScaler()
            scaled = scaler.fit_transform(df_pair)

            pca = PCA(n_components=2)
            pca.fit(scaled)

            explained_ratio = pca.explained_variance_ratio_[0]
            return float(explained_ratio)

        except Exception as e:
            print(f"[PcaRunnerMetric] Error: {e}")
            return np.nan
