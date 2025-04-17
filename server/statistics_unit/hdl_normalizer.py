import pandas as pd
from normalizer import Normalizer
# Example implementation for HDL normalization
class HDLNormalizer(Normalizer):
    def normalize(self, series: pd.Series) -> pd.Series:
        """
        Normalize HDL values using a min-max scaling approach.
        For example, assuming HDL is measured in mg/dL and typical values range between 20 and 100:
          normalized_value = (value - 20) / (100 - 20)
        """
        min_val, max_val = 20, 100
        return (series - min_val) / (max_val - min_val)
