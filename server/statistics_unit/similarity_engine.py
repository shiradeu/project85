import os
import importlib
import inspect
import pandas as pd
from correlations_calc.pair_similarity.base_metric import BaseMetric
from normalize.data_normalizer import DataNormalizer
from sklearn.datasets import load_breast_cancer

class SimilarityEngine:
    def __init__(self, df, metrics_package: str, normalizer_config_path: str):
        self.df_raw = df
        self.metrics_package = metrics_package
        self.normalizer_config_path = normalizer_config_path
        self.metric_classes = self._load_metric_classes()
        self.df_normalized = self._normalize_df()

    def _load_metric_classes(self):
        metric_classes = []
        package_path = self.metrics_package.replace('.', '/')
        for file in os.listdir(package_path):
            if file.endswith('.py') and not file.startswith('__') and file != 'base_metric.py':
                module_name = f"{self.metrics_package}.{file[:-3]}"
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BaseMetric) and obj is not BaseMetric:
                        metric_classes.append(obj)
        return metric_classes

    def _normalize_df(self):
        normalizer = DataNormalizer(self.df_raw, self.normalizer_config_path)
        df_norm = normalizer.runner()
        return df_norm

    def run(self):
        all_cols = self.df_raw.columns
        matrix = pd.DataFrame(index=all_cols, columns=all_cols, dtype=float)

        for col1 in all_cols:
            for col2 in all_cols:
                if col1 == col2:
                    matrix.loc[col1, col2] = 1.0
                    continue

                scores = []

                for MetricClass in self.metric_classes:
                    metric = MetricClass()

                    # Use normalized or raw data based on the metric
                    x = self.df_normalized[col1] if metric.use_normalized else self.df_raw[col1]
                    y = self.df_normalized[col2] if metric.use_normalized else self.df_raw[col2]

                    applicable = metric.is_applicable(x, y)
                    if applicable:
                            score = metric.score(x, y)
                            if pd.notna(score) and pd.api.types.is_number(score):
                                scores.append(score)
                      
                matrix.loc[col1, col2] = sum(scores) / len(scores) if scores else None

        return matrix.round(3)

def top_variable_pairs(similarity_matrix, top_n=10):

        pairs = []
        for i in similarity_matrix.index:
            for j in similarity_matrix.columns:
                if i != j and pd.notna(similarity_matrix.loc[i, j]):
                    pairs.append(((i, j), similarity_matrix.loc[i, j]))
        unique_pairs = {}
        for (var1, var2), score in pairs:
            key = tuple(sorted([var1, var2]))
            if key not in unique_pairs or score > unique_pairs[key]:
                unique_pairs[key] = score
        sorted_pairs = sorted(unique_pairs.items(), key=lambda x: x[1], reverse=True)
        return sorted_pairs[:top_n]
# ================== MAIN ==================

if __name__ == "__main__":

    data = load_breast_cancer()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df["target"] = data.target.astype(str)

    engine = SimilarityEngine(
        df,
        metrics_package="correlations_calc.pair_similarity",
        normalizer_config_path="normalize/normalizers_config.json"
    )
    result = engine.run()

    print(result)
    top_pairs = top_variable_pairs(result, top_n=10)
    print(top_pairs)

    for (var1, var2), score in top_pairs:
        print(f"{var1} - {var2}: {score}")
