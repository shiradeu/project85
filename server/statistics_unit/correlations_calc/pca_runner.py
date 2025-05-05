from .base_metric import BaseMetric
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import mutual_info_regression
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import ttest_ind, chi2_contingency
from scipy.spatial.distance import pdist, squareform
from math import log2

class PcaRunnerMetric(BaseMetric):
    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        try:
            return pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y)
        except:
            return False

    def score(self, x: pd.Series, y: pd.Series) -> float:
        # Original logic below
        import pandas as pd
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler
        from sklearn.datasets import load_iris
        
        class PCARelationAnalyzer:
            def __init__(self, df, n_components=None):
                self.df = df.select_dtypes(include=['int', 'float'])
                self.n_components = n_components
                self.scaled_data = None
                self.pca = None
                self.components_ = None
                self.explained_variance_ = None
        
            def run(self):
                # Standardize the data
                scaler = StandardScaler()
                self.scaled_data = scaler.fit_transform(self.df)
        
                # Fit PCA
                self.pca = PCA(n_components=self.n_components)
                self.pca.fit(self.scaled_data)
        
                # Save results
                self.components_ = pd.DataFrame(
                    self.pca.components_,
                    columns=self.df.columns
                )
                self.explained_variance_ = self.pca.explained_variance_ratio_
        
                return {
                    "components": self.components_,
                    "explained_variance": self.explained_variance_
                }
        
        def main():
            # Load example dataset
            iris = load_iris()
            df_iris = pd.DataFrame(iris.data, columns=iris.feature_names)
        
            print("Loaded Iris dataset:")
            print(df_iris.head())
        
            # Run PCA analysis
            analyzer = PCARelationAnalyzer(df_iris, n_components=2)
            results = analyzer.run()
        
            print("\n--- PCA Components (first 2 PCs) ---")
            print(results["components"])
        
            print("\n--- Explained Variance Ratio ---")
            print(results["explained_variance"])
        
        if __name__ == "__main__":
            main()