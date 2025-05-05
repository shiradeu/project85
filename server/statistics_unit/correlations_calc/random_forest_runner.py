import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import load_breast_cancer

class RandomForestImportance:
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
                    X = self.df[[col1]]
                    y = self.df[col2]
                    model = RandomForestRegressor(n_estimators=100, random_state=0)
                    model.fit(X, y)
                    score = model.score(X, y)
                    matrix.loc[col1, col2] = score
        return matrix.astype(float)

def main():
    data = load_breast_cancer()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    analyzer = RandomForestImportance(df)
    result = analyzer.run()
    print("\n--- Random Forest Pairwise Importance Matrix ---")
    print(result.round(3))

if __name__ == "__main__":
    main()