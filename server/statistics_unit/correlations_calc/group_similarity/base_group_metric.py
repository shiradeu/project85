import pandas as pd
from abc import ABC, abstractmethod

class BaseGroupMetric(ABC):
    use_normalized = True  # default behavior

    @abstractmethod
    def is_applicable(self, X: pd.DataFrame, y: pd.Series) -> bool:
        pass

    @abstractmethod
    def score(self, X: pd.DataFrame, y: pd.Series) -> float:
        pass