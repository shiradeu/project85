import os
import importlib
import inspect
import pandas as pd
from correlations_calc.base_metric import BaseMetric

class SimilarityEngine:
    def __init__(self, df, metrics_package: str):
        self.df = df
        self.metrics_package = metrics_package
        self.metric_classes = self._load_metric_classes()

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

    def run(self):
        all_cols = self.df.columns
        matrix = pd.DataFrame(index=all_cols, columns=all_cols, dtype=float)

        for col1 in all_cols:
            for col2 in all_cols:
                if col1 == col2:
                    matrix.loc[col1, col2] = 1.0
                    continue
                x, y = self.df[col1], self.df[col2]
                scores = []
                for MetricClass in self.metric_classes:
                    metric = MetricClass()
                    if metric.is_applicable(x, y):
                        try:
                            score = metric.score(x, y)
                            if pd.notna(score) and pd.api.types.is_number(score):
                                scores.append(score)
                        except Exception:
                            continue
                matrix.loc[col1, col2] = sum(scores) / len(scores) if scores else None

        return matrix.round(3)


# ================== MAIN ==================

if __name__ == "__main__":
    from sklearn.datasets import load_breast_cancer

    # Load a demo dataset
    data = load_breast_cancer()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df["target"] = data.target.astype(str)  # make one categorical column

    # Run similarity engine
    engine = SimilarityEngine(df, metrics_package="correlations_calc")
    result = engine.run()

    print("\n=== Combined Similarity Matrix ===")
    print(result)
