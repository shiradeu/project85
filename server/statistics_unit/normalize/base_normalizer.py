import pandas as pd

class BaseNormalizer:
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val

    def normalize(self, series: pd.Series) -> pd.Series:
        return (series - self.min_val) / (self.max_val - self.min_val)
