from .base_metric import BaseMetric
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import mutual_info_regression
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import ttest_ind, chi2_contingency
from scipy.spatial.distance import pdist, squareform
from math import log2

class DistanceCorrelationMatrixMetric(BaseMetric):
    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        try:
            return pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y)
        except:
            return False

    def score(self, x: pd.Series, y: pd.Series) -> float:
        # Original logic below
        import pandas as pd
        import numpy as np
        from scipy.spatial.distance import pdist, squareform
        from sklearn.datasets import load_breast_cancer
        
        class DistanceCorrelationMatrix:
            def __init__(self, df):
                self.df = df
                self.num_cols = df.select_dtypes(include=['int', 'float']).columns
        
            def distance_corr(self, X, Y):
                def _distance_covariance(a, b):
                    A = squareform(pdist(a[:, None]))
                    B = squareform(pdist(b[:, None]))
                    A_mean = A.mean(axis=0, keepdims=True)
                    B_mean = B.mean(axis=0, keepdims=True)
                    A_centered = A - A_mean - A_mean.T + A.mean()
                    B_centered = B - B_mean - B_mean.T + B.mean()
                    return np.sqrt((A_centered * B_centered).mean())
        
                dcov = _distance_covariance(X, Y)
                dvar_x = _distance_covariance(X, X)
                dvar_y = _distance_covariance(Y, Y)
                if dvar_x > 0 and dvar_y > 0:
                    return dcov / np.sqrt(dvar_x * dvar_y)
                else:
                    return 0.0
        
            def run(self):
                matrix = pd.DataFrame(index=self.num_cols, columns=self.num_cols)
                for col1 in self.num_cols:
                    for col2 in self.num_cols:
                        if col1 == col2:
                            matrix.loc[col1, col2] = 1.0
                        else:
                            val = self.distance_corr(self.df[col1].values, self.df[col2].values)
                            matrix.loc[col1, col2] = val
                return matrix.astype(float)
        
        def main():
            data = load_breast_cancer()
            df = pd.DataFrame(data.data, columns=data.feature_names)
            analyzer = DistanceCorrelationMatrix(df)
            result = analyzer.run()
            print("\n--- Distance Correlation Matrix ---")
            print(result.round(3))
        
        if __name__ == "__main__":
            main()