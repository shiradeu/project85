import pandas as pd
import numpy as np
from math import log2
from sklearn.datasets import load_iris

class TheilsUMatrix:
    def __init__(self, df):
        self.df = df
        self.cat_cols = df.select_dtypes(include=['object', 'category']).columns

    def conditional_entropy(self, x, y):
        y_counter = y.value_counts()
        xy_counter = pd.crosstab(x, y)
        total_occurrences = len(x)
        entropy = 0.0
        for xi in xy_counter.index:
            for yj in xy_counter.columns:
                p_xy = xy_counter.loc[xi, yj] / total_occurrences
                p_y = y_counter[yj] / total_occurrences
                if p_xy > 0:
                    entropy += p_xy * log2(p_y / p_xy)
        return entropy

    def run(self):
        matrix = pd.DataFrame(index=self.cat_cols, columns=self.cat_cols)
        for col1 in self.cat_cols:
            for col2 in self.cat_cols:
                if col1 == col2:
                    matrix.loc[col1, col2] = 1.0
                else:
                    s1 = self.df[col1].astype(str)
                    s2 = self.df[col2].astype(str)
                    entropy_s1 = self.conditional_entropy(s1, s1)
                    cond_entropy = self.conditional_entropy(s1, s2)
                    if entropy_s1 == 0:
                        matrix.loc[col1, col2] = 0.0
                    else:
                        matrix.loc[col1, col2] = (entropy_s1 - cond_entropy) / entropy_s1
        return matrix.astype(float)

def main():
    data = load_iris()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = pd.Categorical(data.target)
    df['target'] = df['target'].astype(str)

    analyzer = TheilsUMatrix(df)
    result = analyzer.run()
    print("\n--- Theil's U Matrix (Uncertainty Coefficient) ---")
    print(result.round(3))

if __name__ == "__main__":
    main()