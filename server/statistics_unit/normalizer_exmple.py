import pandas as pd
from data_normalizer import DataNormalizer

df = pd.DataFrame({
    "hdl": [40, 60, 80],
    "ldl": [100, 130, 160],
    "potassium": [4, 6, 3]
})

normalizer = DataNormalizer(df, "normalizers_config.json")
normalized_df = normalizer.runner()
print(normalized_df)
