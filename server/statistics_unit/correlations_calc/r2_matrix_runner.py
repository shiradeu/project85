import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_breast_cancer

class R2MatrixRunner:
    def __init__(self, df):
        self.df = df
        self.numeric_cols = df.select_dtypes(include=['int', 'float']).columns

    def run(self):
        matrix = pd.DataFrame(index=self.numeric_cols, columns=self.numeric_cols)
        for col_y in self.numeric_cols:
            for col_x in self.numeric_cols:
                if col_y == col_x:
                    matrix.loc[col_y, col_x] = 1.0
                else:
                    X = self.df[[col_x]]
                    y = self.df[col_y]
                    model = LinearRegression().fit(X, y)
                    r2 = model.score(X, y)
                    matrix.loc[col_y, col_x] = r2
        return matrix.astype(float)

def main():
    data = load_breast_cancer()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    analyzer = R2MatrixAnalyzer(df)
    result = analyzer.run()
    print("\n--- R² Pairwise Matrix (col_y vs col_x) ---")
    print(result.round(3))

if __name__ == "__main__":
    main()
