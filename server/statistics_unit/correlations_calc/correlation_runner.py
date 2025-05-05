import pandas as pd
from scipy.stats import pearsonr
from sklearn.datasets import load_breast_cancer

class CorrelationAnalyzer:
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
                    corr, _ = pearsonr(self.df[col1], self.df[col2])
                    matrix.loc[col1, col2] = abs(corr)
        return matrix.astype(float)

def main():
    data = load_breast_cancer()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    
    analyzer = CorrelationAnalyzer(df)
    result = analyzer.run()
    
    print("\n--- Correlation Matrix ---")
    print(result.round(2))

if __name__ == "__main__":
    main()
