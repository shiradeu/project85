import pandas as pd
from abc import ABC, abstractmethod

class BaseMetric(ABC):
    use_normalized: bool = True  # ניתן לשנות במחלקה היורשת

    @abstractmethod
    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        pass

    @abstractmethod
    def score(self, x: pd.Series, y: pd.Series) -> float:
        pass