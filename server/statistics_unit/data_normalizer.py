import json
from hdl_normalizer import HDLNormalizer
from ldl_normalizer import LDLNormalizer
from potassium_normalizer import PotassiumNormalizer
from sodium_normalizer import SodiumNormalizer
from normalizer import Normalizer  # רק בשביל לוודא שהכל תקני

# מיפוי מחרוזות לשמות המחלקות בפועל
normalizer_classes = {
    "HDLNormalizer": HDLNormalizer,
    "LDLNormalizer": LDLNormalizer,
    "SodiumNormalizer": SodiumNormalizer,
    "PotassiumNormalizer": PotassiumNormalizer
}

class DataNormalizer:
    def __init__(self, df, config_file):
        self.df = df
        self.config_file = config_file

    def runner(self):
        df_copy = self.df.copy()
        with open(self.config_file, 'r') as f:
            config = json.load(f)
            for col in df_copy.columns:
                if col in config:
                    class_name = config[col]
                    if class_name not in normalizer_classes:
                        print(f"Normalizer class '{class_name}' not found.")
                        continue
                    normalizer = normalizer_classes[class_name]()
                    df_copy[col] = normalizer.normalize(df_copy[col])
                    print(f"Normalized column '{col}' using {class_name}.")
                else:
                    print(f"No normalizer configured for column '{col}'.")
        return df_copy
