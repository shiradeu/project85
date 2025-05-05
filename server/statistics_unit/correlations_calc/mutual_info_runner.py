from .base_metric import BaseMetric
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import mutual_info_regression
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import ttest_ind, chi2_contingency
from scipy.spatial.distance import pdist, squareform
from math import log2

class MutualInfoRunnerMetric(BaseMetric):
    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        try:
            return pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y)
        except:
            return False

    def score(self, x: pd.Series, y: pd.Series) -> float:
        # Original logic below
        import pandas as pd
        from sklearn.datasets import load_breast_cancer
        from sklearn.feature_selection import mutual_info_regression  # ← זה מה שהיה חסר
        
        class MutualInfoAnalyzer:
            def __init__(self, df):
                self.df = df
                self.numeric_cols = df.select_dtypes(include=['int', 'float']).columns
        
            def run(self):
                matrix = pd.DataFrame(index=self.numeric_cols, columns=self.numeric_cols)
                for col1 in self.numeric_cols:
                    for col2 in self.numeric_cols:
                        if col1 == col2:
                            matrix.loc[col1, col2] = 1.0
                        else:
                            x = self.df[[col1]]
                            y = self.df[col2]
                            score = mutual_info_regression(x, y, random_state=0)[0]
                            matrix.loc[col1, col2] = score
                return matrix.astype(float)
        
        def main():
            data = load_breast_cancer()
            df = pd.DataFrame(data.data, columns=data.feature_names)
            
            analyzer = MutualInfoAnalyzer(df)
            result = analyzer.run()
            
            print("\n--- Mutual Information Matrix ---")
            print(result.round(2))
        
        if __name__ == "__main__":
            main()