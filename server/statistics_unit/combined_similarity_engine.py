import pandas as pd

class CombinedSimilarityEngine:
    def __init__(self, df, pair_engine, group_engine):
        self.df = df
        self.pair_engine = pair_engine
        self.group_engine = group_engine

    def run(self, top_n=10):
        pair_df = self.pair_engine.run().reset_index()
        pair_df.columns = ["var1", "var2", "score"]
        pair_df["type"] = "pair"

        group_df = self.group_engine.run()
        group_df.columns = ["var1", "var2", "score"]
        group_df["type"] = "group"

        combined = pd.concat([pair_df, group_df], ignore_index=True)

        top_combined = combined.sort_values("score", ascending=False).head(top_n)

        for _, row in top_combined.iterrows():
            var1 = row["var1"]
            var2 = row["var2"]
            var1_str = ", ".join(var1) if isinstance(var1, (list, tuple)) else var1
            print(f"{row['type'].upper()} | {var1_str} → {var2}: {row['score']:.4f}")

        return top_combined
if __name__ == "__main__":
    from sklearn.datasets import load_breast_cancer
    from similarity_engine import SimilarityEngine
    from group_similarity_engine import GroupSimilarityEngine

    df = pd.DataFrame(load_breast_cancer().data, columns=load_breast_cancer().feature_names)

    pair_engine = SimilarityEngine(
        df,
        metrics_package="correlations_calc.pair_similarity",
        normalizer_config_path="normalize/normalizers_config.json"
    )

    group_engine = GroupSimilarityEngine(df, metrics_package="correlations_calc.group_similarity", group_size=2)

    combined_engine = CombinedSimilarityEngine(df, pair_engine, group_engine)
    combined_results = combined_engine.run(top_n=10)
import pandas as pd
from sklearn.datasets import load_breast_cancer
from similarity_engine import SimilarityEngine
from group_similarity_engine import GroupSimilarityEngine

def flatten_similarity_matrix(matrix_df):
    pairs = []
    for i in matrix_df.index:
        for j in matrix_df.columns:
            if i < j and pd.notna(matrix_df.loc[i, j]):
                pairs.append((i, j, matrix_df.loc[i, j]))
    return pd.DataFrame(pairs, columns=["var1", "var2", "score"])

