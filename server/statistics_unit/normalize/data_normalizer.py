import json
from normalize.base_normalizer import BaseNormalizer

class DataNormalizer:
    def __init__(self, df, config_file):
        self.df = df
        self.config_file = config_file

    def runner(self):
        df_copy = self.df.copy()

        with open(self.config_file, 'r') as f:
            config = json.load(f)

        for col in df_copy.columns:
            try:
                if any(key in col for key in config):
                    col_type = next((key for key in config if key in col), None)
                    params = config[col_type]
                    min_val = params["min"]
                    max_val = params["max"]
                else:
                    min_val = df_copy[col].min()
                    max_val = df_copy[col].max()

                normalizer = BaseNormalizer(min_val, max_val)
                df_copy[col] = normalizer.normalize(df_copy[col])

            except Exception as e:
                print(f"Failed to normalize column '{col}': {e}")

        return df_copy
