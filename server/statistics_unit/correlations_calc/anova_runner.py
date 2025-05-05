from .base_metric import BaseMetric
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import mutual_info_regression
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import ttest_ind, chi2_contingency
from scipy.spatial.distance import pdist, squareform
from math import log2

class AnovaRunnerMetric(BaseMetric):
    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        try:
            return pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y)
        except:
            return False

    def score(self, x: pd.Series, y: pd.Series) -> float:
        # Original logic below
        import pandas as pd
        import itertools
        import statsmodels.api as sm
        import statsmodels.formula.api as smf
        import seaborn as sns  # כדי להשתמש בדאטהסט מוכן
        
        def run_anova_tests(df, p_thresh=0.05):
            results = []
        
            # נזהה משתנים
            categorical_cols = [
                col for col in df.select_dtypes(include=['object', 'category']).columns
                if df[col].nunique() < 20  # גבול סביר לקטגוריה
            ]
            numeric_cols = df.select_dtypes(include=['int', 'float']).columns
        
            # One-Way ANOVA
            for cat in categorical_cols:
                for num in numeric_cols:
                    try:
                        model = smf.ols(f"{num} ~ C({cat})", data=df).fit()
                        anova_table = sm.stats.anova_lm(model, typ=2)
                        p_value = anova_table["PR(>F)"][0]
                        if p_value < p_thresh:
                            results.append({
                                "type": "one-way",
                                "dependent": num,
                                "independent": [cat],
                                "p_value": p_value
                            })
                    except Exception as e:
                        print(f"Failed one-way for {num} ~ {cat}: {e}")
        
            # Two-Way ANOVA
            for cat1, cat2 in itertools.combinations(categorical_cols, 2):
                for num in numeric_cols:
                    try:
                        formula = f"{num} ~ C({cat1}) + C({cat2}) + C({cat1}):C({cat2})"
                        model = smf.ols(formula, data=df).fit()
                        anova_table = sm.stats.anova_lm(model, typ=2)
                        p_values = anova_table["PR(>F)"].to_dict()
        
                        # נשמור רק אם לפחות אחד מהאפקטים מובהק
                        if any(p < p_thresh for p in p_values.values()):
                            results.append({
                                "type": "two-way",
                                "dependent": num,
                                "independent": [cat1, cat2],
                                "p_values": p_values
                            })
                    except Exception as e:
                        print(f"Failed two-way for {num} ~ {cat1}*{cat2}: {e}")
        
            # בניית DataFrame מהתוצאות
            df_results = pd.DataFrame(results)
        
            # הוספת עמודת p-value הראשית למיון
            def extract_min_p(row):
                if row["type"] == "one-way":
                    return row["p_value"]
                else:
                    return min(row["p_values"].values())
        
            if not df_results.empty:
                df_results["min_p"] = df_results.apply(extract_min_p, axis=1)
                df_results = df_results.sort_values("min_p")
        
            return df_results
            results = []
        
            # נזהה משתנים
            categorical_cols = [
                col for col in df.select_dtypes(include=['object', 'category']).columns
                if df[col].nunique() < 20  # גבול סביר לקטגוריה
            ]
            numeric_cols = df.select_dtypes(include=['int', 'float']).columns
        
            # One-Way ANOVA
            for cat in categorical_cols:
                for num in numeric_cols:
                    try:
                        model = smf.ols(f"{num} ~ C({cat})", data=df).fit()
                        anova_table = sm.stats.anova_lm(model, typ=2)
                        p_value = anova_table["PR(>F)"][0]
                        results.append({
                            "type": "one-way",
                            "dependent": num,
                            "independent": [cat],
                            "p_value": p_value
                        })
                    except Exception as e:
                        print(f"Failed one-way for {num} ~ {cat}: {e}")
        
            # Two-Way ANOVA
            for cat1, cat2 in itertools.combinations(categorical_cols, 2):
                for num in numeric_cols:
                    try:
                        formula = f"{num} ~ C({cat1}) + C({cat2}) + C({cat1}):C({cat2})"
                        model = smf.ols(formula, data=df).fit()
                        anova_table = sm.stats.anova_lm(model, typ=2)
                        results.append({
                            "type": "two-way",
                            "dependent": num,
                            "independent": [cat1, cat2],
                            "p_values": anova_table["PR(>F)"].to_dict()
                        })
                    except Exception as e:
                        print(f"Failed two-way for {num} ~ {cat1}*{cat2}: {e}")
        
            return pd.DataFrame(results)
        
        def main():
            # נשתמש בדאטהסט של seaborn לדוגמה
            df = sns.load_dataset("tips")
            print("Loaded dataset: tips")
            print(df.head())
        
            # הרצת מבחני אנובה
            anova_results = run_anova_tests(df)
        
            print("\n--- ANOVA Results ---")
            print(anova_results)
        
        if __name__ == "__main__":
            main()