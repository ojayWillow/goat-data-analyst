from typing import Dict, List, Optional
import pandas as pd


class ProfileIntelligence:
    """Extracts meaningful insights from DataProfiler results to guide chart generation."""
    
    def __init__(self, df: pd.DataFrame, profile: Dict):
        self.df = df
        self.profile = profile
    
    def get_key_numeric_columns(self, max_cols: int = 3) -> List[str]:
        """Find most meaningful numeric columns (skip IDs)."""
        candidates = []
        
        for col in self.df.select_dtypes(include=['number']).columns:
            # Skip if name suggests ID
            col_lower = col.lower()
            if any(x in col_lower for x in ['_id', 'id', 'index']):
                continue
            
            # Check if has any variation at all
            if self.df[col].nunique() == 1:
                continue
            
            unique_ratio = self.df[col].nunique() / len(self.df)
            
            # Skip ONLY if very high uniqueness AND small value range (likely sequential ID)
            if unique_ratio > 0.95:
                # Check if values are sequential (strong ID indicator)
                sorted_vals = sorted(self.df[col].dropna().unique())
                if len(sorted_vals) > 1:
                    diffs = [sorted_vals[i+1] - sorted_vals[i] for i in range(len(sorted_vals)-1)]
                    avg_diff = sum(diffs) / len(diffs)
                    # If mostly incrementing by 1, it's likely an ID
                    if avg_diff <= 2:
                        continue
            
            # If we got here, it's a valid numeric column
            # Score by data range (prefer columns with meaningful variation)
            data_range = self.df[col].max() - self.df[col].min()
            score = data_range if data_range > 0 else 1
            
            candidates.append((score, col))
        
        # Return top N by score
        candidates.sort(reverse=True)
        return [col for score, col in candidates[:max_cols]]
    
    def get_key_categorical_columns(self, max_cols: int = 2) -> List[str]:
        """Find most meaningful categorical columns (reasonable cardinality)."""
        candidates = []
        
        for col in self.df.select_dtypes(include=['object', 'category']).columns:
            # Skip if name suggests ID
            col_lower = col.lower()
            if any(x in col_lower for x in ['_id', 'id']):
                continue
            
            n_unique = self.df[col].nunique()
            unique_ratio = n_unique / len(self.df)
            
            # Skip if too unique (>90% = likely ID)
            if unique_ratio > 0.90:
                continue
            
            # Only if reasonable cardinality
            if not (2 <= n_unique <= 50):
                continue
            
            # Score: prefer 5-15 categories
            if 5 <= n_unique <= 15:
                score = 100
            elif 3 <= n_unique <= 20:
                score = 80
            else:
                score = 50
            
            candidates.append((score, col))
        
        # Return top N by score
        candidates.sort(reverse=True)
        return [col for score, col in candidates[:max_cols]]
    
    def get_datetime_columns(self) -> List[str]:
        """Find datetime columns."""
        datetime_cols = []
        
        for col in self.df.columns:
            if pd.api.types.is_datetime64_any_dtype(self.df[col]):
                datetime_cols.append(col)
        
        return datetime_cols
    
    def should_generate_chart(self, chart_type: str) -> bool:
        """Determine if a chart type is relevant for this dataset."""
        if chart_type == "time_series":
            return len(self.get_datetime_columns()) > 0
        
        elif chart_type == "distribution":
            return len(self.get_key_numeric_columns(max_cols=1)) > 0
        
        elif chart_type == "correlation":
            return len(self.get_key_numeric_columns(max_cols=2)) >= 2
        
        elif chart_type == "category":
            return len(self.get_key_categorical_columns(max_cols=1)) > 0
        
        return False
