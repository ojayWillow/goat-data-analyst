from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd


class BaseChart(ABC):
    """Abstract base class for all chart generators."""
    
    def __init__(self, df: pd.DataFrame, domain: Optional[str] = None):
        self.df = df
        self.domain = domain
    
    @abstractmethod
    def can_generate(self) -> bool:
        """
        Check if this chart is applicable to the current dataset.
        Returns True if chart should be generated.
        """
        pass
    
    @abstractmethod
    def generate(self) -> str:
        """
        Generate the chart HTML.
        Returns empty string if chart cannot be generated.
        """
        pass
    
    @property
    @abstractmethod
    def chart_name(self) -> str:
        """Unique identifier for this chart type."""
        pass
