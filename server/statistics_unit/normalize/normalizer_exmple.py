import pandas as pd
from normalize.data_normalizer import DataNormalizer
df = pd.DataFrame({
    "hdl": [40, 60, 80],
    "ldl": [100, 130, 160],
    "potassium": [4, 6, 3],
    "insulinush": [40, 16, 23],
    
})

normalizer = DataNormalizer(df, "normalize/normalizers_config.json")
normalized_df = normalizer.runner()
print(normalized_df)
