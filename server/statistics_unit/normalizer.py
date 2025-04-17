from abc import ABC, abstractmethod
import pandas as pd

# Define an interface using an abstract base class
class Normalizer(ABC):
    @abstractmethod
    def normalize(self, series: pd.Series) -> pd.Series:
        """Normalize the given pandas Series."""
        pass