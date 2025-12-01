"""
Universal Chart Generator
Generates Plotly charts for data visualization
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime


class UniversalChartGenerator:
    """Generate universal charts for any dataset."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with dataframe."""
        self.df = df
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # Try to identify date columns in object type
        if not self.date_cols:
            for col in self.categorical_cols:
                try:
                    parsed = pd.to_datetime(col, format='mixed', errors='coerce')
                    if parsed.notna().sum() > len(df) * 0.8:
                        self.date_cols.append(col)
                except:
                    pass
    
    def _get_date_column(self) -> Optional[str]:
        """Get the first date column."""
        if self.date_cols:
            return self.date_cols[0]
        
        # Try to parse categorical columns as dates
        for col in self.categorical_cols:
            try:
                pd.to_datetime(self.df[col], format='mixed', errors='coerce')
                return col
            except:
                pass
        
        return None
    
    def _get_numeric_column(self) -> Optional[str]:
        """Get the first numeric column."""
        return self.numeric_cols[0] if self.numeric_cols else None
    
    def _get_categorical_column(self) -> Optional[str]:
        """Get the first categorical column."""
        return self.categorical_cols[0] if self.categorical_cols else None
    
    def create_volume_over_time(self) -> str:
        """
        Create time series chart showing volume/values over time.
        Requires at least one date column and one numeric column.
        """
        try:
            date_col = self._get_date_column()
            numeric_col = self._get_numeric_column()
            
            if not date_col or not numeric_col:
                return ""
            
            # Prepare data
            df_temp = self.df.copy()
            df_temp[date_col] = pd.to_datetime(df_temp[date_col], format='mixed', errors='coerce')
            df_temp = df_temp.dropna(subset=[date_col, numeric_col])
            
            if len(df_temp) == 0:
                return ""
            
            df_temp = df_temp.sort_values(date_col)
            
            # Create figure
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df_temp[date_col],
                y=df_temp[numeric_col],
                mode='lines+markers',
                name=numeric_col,
                line=dict(
                    color='rgb(33, 128, 141)',
                    width=3
                ),
                marker=dict(
                    size=8,
                    color='rgb(33, 128, 141)',
                    opacity=0.8
                ),
                hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                              f'{numeric_col}: %{{y:.2f}}<extra></extra>'
            ))
            
            fig.update_layout(
                title={
                    'text': f'<b>{numeric_col} Over Time</b>',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18}
                },
                xaxis_title=date_col,
                yaxis_title=numeric_col,
                template='plotly_white',
                height=450,
                hovermode='x unified',
                margin=dict(l=60, r=40, t=60, b=60),
                plot_bgcolor='rgba(240, 240, 240, 0.5)',
                xaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='lightgray'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='lightgray'
                )
            )
            
            return fig.to_html(
                include_plotlyjs=False,
                div_id=f"chart_time_series_{abs(hash(numeric_col)) % 10000}"
            )
        
        except Exception as e:
            return f"<div style='color: red; padding: 20px;'>Error generating time series: {str(e)[:50]}</div>"
    
    def create_smart_distribution(self) -> str:
        """
        Create distribution chart for numeric columns.
        Shows histogram of values.
        """
        try:
            numeric_col = self._get_numeric_column()
            
            if not numeric_col:
                return ""
            
            # Remove NaN values
            data = self.df[numeric_col].dropna()
            
            if len(data) == 0:
                return ""
            
            # Determine number of bins
            nbins = min(30, max(10, len(data) // 5))
            
            fig = go.Figure()
            
            fig.add_trace(go.Histogram(
                x=data,
                nbinsx=nbins,
                name=numeric_col,
                marker=dict(
                    color='rgb(33, 128, 141)',
                    line=dict(color='rgb(20, 90, 100)', width=1)
                ),
                opacity=0.8,
                hovertemplate='Range: %{x}<br>Count: %{y}<extra></extra>'
            ))
            
            fig.update_layout(
                title={
                    'text': f'<b>Distribution of {numeric_col}</b>',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18}
                },
                xaxis_title=numeric_col,
                yaxis_title='Frequency',
                template='plotly_white',
                height=450,
                hovermode='x unified',
                margin=dict(l=60, r=40, t=60, b=60),
                plot_bgcolor='rgba(240, 240, 240, 0.5)',
                xaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='lightgray'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='lightgray'
                )
            )
            
            return fig.to_html(
                include_plotlyjs=False,
                div_id=f"chart_distribution_{abs(hash(numeric_col)) % 10000}"
            )
        
        except Exception as e:
            return f"<div style='color: red; padding: 20px;'>Error generating distribution: {str(e)[:50]}</div>"
    
    def create_correlation_heatmap(self) -> str:
        """
        Create correlation matrix heatmap for numeric columns.
        Shows relationships between variables.
        """
        try:
            if len(self.numeric_cols) < 2:
                return ""
            
            # Calculate correlation
            corr_matrix = self.df[self.numeric_cols].corr()
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                zmin=-1,
                zmax=1,
                text=np.round(corr_matrix.values, 2),
                texttemplate='%{text:.2f}',
                textfont={"size": 11},
                colorbar=dict(title="Correlation", thickness=20, len=0.7),
                hovertemplate='%{y} vs %{x}<br>Correlation: %{z:.3f}<extra></extra>'
            ))
            
            fig.update_layout(
                title={
                    'text': '<b>Correlation Matrix</b>',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18}
                },
                xaxis_title='Variables',
                yaxis_title='Variables',
                height=500,
                width=550,
                template='plotly_white',
                margin=dict(l=80, r=100, t=60, b=80)
            )
            
            return fig.to_html(
                include_plotlyjs=False,
                div_id=f"chart_correlation_{abs(hash(str(corr_matrix.columns))) % 10000}"
            )
        
        except Exception as e:
            return f"<div style='color: red; padding: 20px;'>Error generating correlation: {str(e)[:50]}</div>"
    
    def create_category_breakdown(self) -> str:
        """
        Create bar chart showing breakdown by category.
        Shows top categories by count.
        """
        try:
            cat_col = self._get_categorical_column()
            
            if not cat_col:
                return ""
            
            # Get value counts
            value_counts = self.df[cat_col].value_counts().head(15)
            
            if len(value_counts) == 0:
                return ""
            
            # Create bar chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=value_counts.index.astype(str),
                y=value_counts.values,
                marker=dict(
                    color='rgb(33, 128, 141)',
                    line=dict(color='rgb(20, 90, 100)', width=1)
                ),
                text=value_counts.values,
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
            ))
            
            fig.update_layout(
                title={
                    'text': f'<b>Top Categories in {cat_col}</b>',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18}
                },
                xaxis_title=cat_col,
                yaxis_title='Count',
                template='plotly_white',
                height=450,
                hovermode='x unified',
                margin=dict(l=60, r=40, t=60, b=80),
                plot_bgcolor='rgba(240, 240, 240, 0.5)',
                xaxis=dict(
                    showgrid=False,
                    tickangle=-45
                ),
                yaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='lightgray'
                )
            )
            
            return fig.to_html(
                include_plotlyjs=False,
                div_id=f"chart_categories_{abs(hash(cat_col)) % 10000}"
            )
        
        except Exception as e:
            return f"<div style='color: red; padding: 20px;'>Error generating category breakdown: {str(e)[:50]}</div>"
    
    def generate_all_universal_charts(self) -> Dict[str, str]:
        """
        Generate all available charts for the dataset.
        Returns dictionary with chart HTML strings.
        """
        charts = {
            'time_series': self.create_volume_over_time(),
            'distribution': self.create_smart_distribution(),
            'correlation': self.create_correlation_heatmap(),
            'category': self.create_category_breakdown()
        }
        
        # Filter out empty charts
        return {k: v for k, v in charts.items() if v}
