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