"""Universal Charts - Domain-agnostic visualizations using Plotly"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional, Any
import numpy as np


class UniversalChartGenerator:
    """Generate adaptive charts that work with any domain."""
    
    def __init__(self, df: pd.DataFrame, domain: str = None):
        self.df = df
        self.domain = domain
        self.charts = {}
    
    def generate_all_charts(self) -> Dict[str, str]:
        """Generate all applicable charts for the dataset."""
        
        # 1. Time series trend (if date column exists)
        time_chart = self._create_time_series()
        if time_chart:
            self.charts['time_series'] = time_chart
        
        # 2. Top N bar chart (categorical + numeric)
        top_n_chart = self._create_top_n_bar()
        if top_n_chart:
            self.charts['top_n'] = top_n_chart
        
        # 3. Distribution chart (numeric columns)
        dist_chart = self._create_distribution()
        if dist_chart:
            self.charts['distribution'] = dist_chart
        
        # 4. Correlation heatmap (numeric columns)
        corr_chart = self._create_correlation()
        if corr_chart:
            self.charts['correlation'] = corr_chart
        
        return self.charts
    
    def _detect_date_column(self) -> Optional[str]:
        """Find the first date/datetime column."""
        for col in self.df.columns:
            if pd.api.types.is_datetime64_any_dtype(self.df[col]):
                return col
            # Try to parse as date
            try:
                pd.to_datetime(self.df[col].head(10))
                return col
            except:
                continue
        return None
    
    def _detect_value_column(self) -> Optional[str]:
        """Find the best numeric column for values (revenue, amount, etc)."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Priority keywords for value columns
        value_keywords = ['revenue', 'amount', 'sales', 'total', 'value', 'price', 'cost']
        
        for keyword in value_keywords:
            for col in numeric_cols:
                if keyword in col.lower():
                    return col
        
        # Return first numeric column if no keyword match
        return numeric_cols[0] if numeric_cols else None
    
    def _detect_category_column(self) -> Optional[str]:
        """Find the best categorical column (customer, product, category)."""
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Priority keywords
        cat_keywords = ['customer', 'product', 'category', 'name', 'type', 'region', 'country']
        
        for keyword in cat_keywords:
            for col in categorical_cols:
                if keyword in col.lower():
                    return col
        
        # Return first categorical column
        return categorical_cols[0] if categorical_cols else None
    
    def _create_time_series(self) -> Optional[str]:
        """Create time series trend chart."""
        date_col = self._detect_date_column()
        value_col = self._detect_value_column()
        
        if not date_col or not value_col:
            return None
        
        try:
            # Prepare data
            df_temp = self.df[[date_col, value_col]].copy()
            df_temp[date_col] = pd.to_datetime(df_temp[date_col])
            df_temp = df_temp.sort_values(date_col)
            
            # Group by date (handle duplicates)
            df_grouped = df_temp.groupby(date_col)[value_col].sum().reset_index()
            
            # Create chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_grouped[date_col],
                y=df_grouped[value_col],
                mode='lines+markers',
                name=value_col,
                line=dict(color='#667eea', width=3),
                marker=dict(size=6)
            ))
            
            fig.update_layout(
                title=f'{value_col} Over Time',
                xaxis_title=date_col,
                yaxis_title=value_col,
                template='plotly_white',
                height=400,
                hovermode='x unified'
            )
            
            return fig.to_html(include_plotlyjs='cdn', div_id='time_series_chart')
        
        except Exception as e:
            print(f"Time series chart error: {e}")
            return None
    
    def _create_top_n_bar(self, n=10) -> Optional[str]:
        """Create Top N bar chart (customers, products, etc)."""
        cat_col = self._detect_category_column()
        value_col = self._detect_value_column()
        
        if not cat_col or not value_col:
            return None
        
        try:
            # Aggregate and get top N
            df_agg = self.df.groupby(cat_col)[value_col].sum().reset_index()
            df_top = df_agg.nlargest(n, value_col)
            
            # Create chart
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df_top[value_col],
                y=df_top[cat_col],
                orientation='h',
                marker=dict(
                    color=df_top[value_col],
                    colorscale='Viridis',
                    showscale=True
                )
            ))
            
            fig.update_layout(
                title=f'Top {n} {cat_col} by {value_col}',
                xaxis_title=value_col,
                yaxis_title=cat_col,
                template='plotly_white',
                height=400,
                yaxis=dict(autorange="reversed")
            )
            
            return fig.to_html(include_plotlyjs='cdn', div_id='top_n_chart')
        
        except Exception as e:
            print(f"Top N chart error: {e}")
            return None
    
    def _create_distribution(self) -> Optional[str]:
        """Create distribution histogram for main numeric column."""
        value_col = self._detect_value_column()
        
        if not value_col:
            return None
        
        try:
            # Create histogram
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=self.df[value_col],
                nbinsx=30,
                marker=dict(color='#667eea'),
                name=value_col
            ))
            
            fig.update_layout(
                title=f'Distribution of {value_col}',
                xaxis_title=value_col,
                yaxis_title='Frequency',
                template='plotly_white',
                height=400
            )
            
            return fig.to_html(include_plotlyjs='cdn', div_id='distribution_chart')
        
        except Exception as e:
            print(f"Distribution chart error: {e}")
            return None
    
    def _create_correlation(self) -> Optional[str]:
        """Create correlation heatmap for numeric columns."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) < 2:
            return None
        
        try:
            # Limit to max 10 columns for readability
            cols_to_use = numeric_cols[:10]
            corr_matrix = self.df[cols_to_use].corr()
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=corr_matrix.values.round(2),
                texttemplate='%{text}',
                textfont={"size": 10},
                colorbar=dict(title="Correlation")
            ))
            
            fig.update_layout(
                title='Correlation Heatmap',
                template='plotly_white',
                height=500,
                xaxis=dict(tickangle=-45)
            )
            
            return fig.to_html(include_plotlyjs='cdn', div_id='correlation_chart')
        
        except Exception as e:
            print(f"Correlation chart error: {e}")
            return None
