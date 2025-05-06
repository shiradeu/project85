import pandas as pd
import itertools
import numpy as np
import importlib
import inspect
import os
from sklearn.datasets import load_breast_cancer

from correlations_calc.group_similarity.base_group_metric import BaseGroupMetric

class GroupSimilarityEngine:
    def __init__(self, df, metrics_package='group_metrics', group_size=2):
        self.df = df
        self.metrics_package = metrics_package
        self.group_size = group_size
        self.metric_classes = self._load_metric_classes()

    def _load_metric_classes(self):
        metric_classes = []
        package_path = self.metrics_package.replace('.', '/')
        for file in os.listdir(package_path):
            if file.endswith('.py') and not file.startswith('__') and file != 'base_group_metric.py':
                module_name = f"{self.metrics_package}.{file[:-3]}"
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BaseGroupMetric) and obj is not BaseGroupMetric:
                        metric_classes.append(obj)
        return metric_classes

    def run(self):
        columns = self.df.select_dtypes(include=[np.number]).columns
        results = []

        for predictors in itertools.combinations(columns, self.group_size):
            target_candidates = [col for col in columns if col not in predictors]
            for target in target_candidates:
                X = self.df[list(predictors)]
                y = self.df[target]
                scores = []

                for MetricClass in self.metric_classes:
                    metric = MetricClass()
                    if metric.is_applicable(X, y):
                        score = metric.score(X, y)
                        if pd.notna(score):
                            scores.append(score)

                if scores:
                    avg_score = sum(scores) / len(scores)
                    results.append((predictors, target, avg_score))

        return pd.DataFrame(results, columns=["predictors", "target", "score"])
if __name__ == "__main__":

    data = load_breast_cancer()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    engine = GroupSimilarityEngine(df, metrics_package="correlations_calc.group_similarity", group_size=2)
    result_df = engine.run()

    top_results = result_df.sort_values(by="score", ascending=False).head(10)
    for _, row in top_results.iterrows():
        print(f"Predictors: {row['predictors']} -> Target: {row['target']}, Score: {row['score']:.4f}")
