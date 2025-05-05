from abc import ABC, abstractmethod
import pandas as pd

class BaseMetric(ABC):
    @abstractmethod
    def is_applicable(self, x: pd.Series, y: pd.Series) -> bool:
        pass

    @abstractmethod
    def score(self, x: pd.Series, y: pd.Series) -> float:
        pass