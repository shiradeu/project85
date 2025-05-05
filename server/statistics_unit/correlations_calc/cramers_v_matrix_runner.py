from .base_metric import BaseMetric
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import mutual_info_regression
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import ttest_ind, chi2_contingency
from scipy.spatial.distance import pdist, squareform
from math import log2

class CramersVMatrixRunnerMetric(BaseMetric):
    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        try:
            return pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y)
        except:
            return False

    def score(self, x: pd.Series, y: pd.Series) -> float:
        # Original logic below
        import pandas as pd
        import numpy as np
        from scipy.stats import chi2_contingency
        from sklearn.datasets import load_iris
        
        class CramersVMatrix:
            def __init__(self, df):
                self.df = df
                self.cat_cols = df.select_dtypes(include=['object', 'category']).columns
        
            def run(self):
                matrix = pd.DataFrame(index=self.cat_cols, columns=self.cat_cols)
                for col1 in self.cat_cols:
                    for col2 in self.cat_cols:
                        if col1 == col2:
                            matrix.loc[col1, col2] = 1.0
                        else:
                            contingency = pd.crosstab(self.df[col1], self.df[col2])
                            try:
                                chi2, _, _, _ = chi2_contingency(contingency)
                                n = contingency.sum().sum()
                                r, k = contingency.shape
                                v = np.sqrt(chi2 / (n * (min(k, r) - 1)))
                                matrix.loc[col1, col2] = v
                            except:
                                matrix.loc[col1, col2] = np.nan
                return matrix.astype(float)
        
        def main():
            # Load iris dataset and convert numeric target to category
            data = load_iris()
            df = pd.DataFrame(data.data, columns=data.feature_names)
            df['target'] = pd.Categorical(data.target)
            df['target'] = df['target'].astype(str)
        
            analyzer = CramersVMatrix(df)
            result = analyzer.run()
            print("\n--- Cramér's V Matrix (Categorical Only) ---")
            print(result.round(3))
        
        if __name__ == "__main__":
            main()