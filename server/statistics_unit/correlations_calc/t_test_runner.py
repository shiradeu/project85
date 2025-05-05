import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
from sklearn.datasets import load_breast_cancer

class TTestMatrix:
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
                    median = self.df[col2].median()
                    group1 = self.df[self.df[col2] >= median][col1]
                    group2 = self.df[self.df[col2] < median][col1]
                    p_value = ttest_ind(group1, group2, nan_policy='omit')[1]
                    matrix.loc[col1, col2] = 1 - p_value
        return matrix.astype(float)

def main():
    data = load_breast_cancer()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    analyzer = TTestMatrix(df)
    result = analyzer.run()
    print("\n--- T-Test Pairwise Significance Matrix ---")
    print(result.round(3))

if __name__ == "__main__":
    main()
