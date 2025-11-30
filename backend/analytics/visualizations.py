"""
Visualizations Module
Generates interactive charts for data insights using Plotly.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional, Any
from datetime import datetime


class DataVisualizer:
    """
    Creates interactive visualizations for business data.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize visualizer with a DataFrame.
        
        Args:
            df: Pandas DataFrame to visualize
        """
        self.df = df
        self.charts = {}

    def generate_all_charts(self) -> Dict[str, str]:
        """
        Generate all applicable charts based on data.
        
        Returns:
            Dictionary of chart names to HTML strings
        """
        self.charts = {}
        
        # Try to generate each chart type
        revenue_chart = self.create_revenue_trend_chart()
        if revenue_chart:
            self.charts['revenue_trend'] = revenue_chart
        
        top_customers_chart = self.create_top_customers_chart()
        if top_customers_chart:
            self.charts['top_customers'] = top_customers_chart
        
        top_products_chart = self.create_top_products_chart()
        if top_products_chart:
            self.charts['top_products'] = top_products_chart
        
        return self.charts

    def create_revenue_trend_chart(self) -> Optional[str]:
        """
        Create revenue over time line chart.
        
        Returns:
            HTML string of the chart, or None if not applicable
        """
        # Find date and revenue columns
        date_col = self._find_date_column()
        revenue_col = self._find_revenue_column()
        
        if not date_col or not revenue_col:
            return None
        
        try:
            # Prepare data
            df_sorted = self.df[[date_col, revenue_col]].copy()
            df_sorted[date_col] = pd.to_datetime(df_sorted[date_col], errors='coerce')
            df_sorted = df_sorted.dropna()
            df_sorted = df_sorted.sort_values(date_col)
            
            # Group by date and sum revenue
            daily_revenue = df_sorted.groupby(date_col)[revenue_col].sum().reset_index()
            
            # Create chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_revenue[date_col],
                y=daily_revenue[revenue_col],
                mode='lines+markers',
                name='Revenue',
                line=dict(color='#2E86AB', width=2),
                marker=dict(size=6)
            ))
            
            fig.update_layout(
                title='Revenue Trend Over Time',
                xaxis_title='Date',
                yaxis_title='Revenue',
                hovermode='x unified',
                template='plotly_white',
                height=400
            )
            
            return fig.to_html(include_plotlyjs='cdn', div_id='revenue_trend_chart')
        
        except Exception as e:
            print(f"Could not create revenue trend chart: {e}")
            return None

    def create_top_customers_chart(self, top_n: int = 10) -> Optional[str]:
        """
        Create top customers by revenue bar chart.
        
        Args:
            top_n: Number of top customers to show
        
        Returns:
            HTML string of the chart, or None if not applicable
        """
        customer_col = self._find_customer_column()
        revenue_col = self._find_revenue_column()
        
        if not customer_col or not revenue_col:
            return None
        
        try:
            # Group by customer and sum revenue
            customer_revenue = self.df.groupby(customer_col)[revenue_col].sum().reset_index()
            customer_revenue = customer_revenue.sort_values(revenue_col, ascending=False).head(top_n)
            
            # Create chart
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=customer_revenue[customer_col],
                x=customer_revenue[revenue_col],
                orientation='h',
                marker=dict(color='#A23B72'),
                text=customer_revenue[revenue_col].round(2),
                textposition='outside'
            ))
            
            fig.update_layout(
                title=f'Top {top_n} Customers by Revenue',
                xaxis_title='Revenue',
                yaxis_title='Customer',
                template='plotly_white',
                height=400,
                yaxis=dict(autorange='reversed')
            )
            
            return fig.to_html(include_plotlyjs='cdn', div_id='top_customers_chart')
        
        except Exception as e:
            print(f"Could not create top customers chart: {e}")
            return None

    def create_top_products_chart(self, top_n: int = 10) -> Optional[str]:
        """
        Create top products by revenue bar chart.
        
        Args:
            top_n: Number of top products to show
        
        Returns:
            HTML string of the chart, or None if not applicable
        """
        product_col = self._find_product_column()
        revenue_col = self._find_revenue_column()
        
        if not product_col or not revenue_col:
            return None
        
        try:
            # Group by product and sum revenue
            product_revenue = self.df.groupby(product_col)[revenue_col].sum().reset_index()
            product_revenue = product_revenue.sort_values(revenue_col, ascending=False).head(top_n)
            
            # Create chart
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=product_revenue[product_col],
                x=product_revenue[revenue_col],
                orientation='h',
                marker=dict(color='#F18F01'),
                text=product_revenue[revenue_col].round(2),
                textposition='outside'
            ))
            
            fig.update_layout(
                title=f'Top {top_n} Products by Revenue',
                xaxis_title='Revenue',
                yaxis_title='Product',
                template='plotly_white',
                height=400,
                yaxis=dict(autorange='reversed')
            )
            
            return fig.to_html(include_plotlyjs='cdn', div_id='top_products_chart')
        
        except Exception as e:
            print(f"Could not create top products chart: {e}")
            return None

    def _find_date_column(self) -> Optional[str]:
        """Find the most likely date column."""
        date_keywords = ['date', 'time', 'timestamp', 'created', 'order_date', 'purchase_date']
        
        for col in self.df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in date_keywords):
                return col
        
        # Check for datetime dtypes
        for col in self.df.columns:
            if pd.api.types.is_datetime64_any_dtype(self.df[col]):
                return col
        
        return None

    def _find_revenue_column(self) -> Optional[str]:
        """Find the most likely revenue/amount column."""
        revenue_keywords = ['revenue', 'amount', 'total', 'price', 'sales', 'value', 'cost']
        
        for col in self.df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in revenue_keywords):
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    return col
        
        return None

    def _find_customer_column(self) -> Optional[str]:
        """Find the most likely customer column."""
        customer_keywords = ['customer', 'client', 'user', 'buyer', 'account']
        
        for col in self.df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in customer_keywords):
                return col
        
        return None

    def _find_product_column(self) -> Optional[str]:
        """Find the most likely product column."""
        product_keywords = ['product', 'item', 'sku', 'article', 'goods', 'service']
        
        for col in self.df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in product_keywords):
                return col
        
        return None
