import pandas as pd
from normalizer import Normalizer
# Example implementation for HDL normalization
class SodiumNormalizer(Normalizer):
    def normalize(self, series: pd.Series) -> pd.Series:
        """
        Normalize Potassium values using a min-max scaling approach.
        For example, assuming Potassium is measured in mg/dL and typical values range between  3.5 and  5.5:
        """
        min_val, max_val = 135, 145
        return (series - min_val) / (max_val - min_val)
