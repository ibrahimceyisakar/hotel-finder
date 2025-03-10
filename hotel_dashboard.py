import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

# Function to extract numeric values from price strings
def extract_numeric_value(price_str):
    if not price_str or not isinstance(price_str, str):
        return None
    
    matches = re.findall(r'[\d.,]+', price_str)
    if not matches:
        return None
    
    price_text = matches[0]
    price_text = price_text.replace('.', '').replace(',', '.')
    
    try:
        return float(price_text)
    except ValueError:
        return None

# Load and process data
def load_and_process_data(json_file, top_n=10):
    # Load data
    with open(json_file, 'r', encoding='utf-8') as f:
        hotels = json.load(f)
    
    # Convert to DataFrame
    df = pd.DataFrame(hotels)
    
    # Process numeric fields
    df['numeric_price'] = df['price'].apply(extract_numeric_value)
    df['numeric_daily_price'] = df['daily_price'].apply(extract_numeric_value)
    df['numeric_review_score'] = pd.to_numeric(df['review_score'], errors='coerce')
    df['numeric_review_count'] = pd.to_numeric(df['review_count'], errors='coerce')
    
    # Sort by value_ratio
    df = df.sort_values('value_ratio', ascending=False)
    
    # Get top N or all hotels if there are fewer than top_n
    available_hotels = min(top_n, len(df))
    df = df.head(available_hotels)
    
    return df

# Create value overview visualizations
def create_value_overview(df):
    # Value ratio bar chart
    fig_value = px.bar(
        df, 
        y='name', 
        x='value_ratio',
        orientation='h',
        title="Hotels by Value Ratio",
        color='value_ratio',
        color_continuous_scale='Viridis',
        hover_data=['price', 'review_score', 'star_rating'],
        height=500
    )
    
    # Price vs Score scatter plot
    fig_scatter = px.scatter(
        df,
        x='numeric_price',
        y='numeric_review_score',
        color='value_ratio',
        size='numeric_review_count',
        hover_name='name',
        title="Price vs. Review Score",
        labels={
            'numeric_price': 'Price (TL)',
            'numeric_review_score': 'Review Score'
        },
        height=500
    )
    
    return fig_value, fig_scatter

# Create price analysis visualizations
def create_price_analysis(df):
    # Price distribution
    fig_price_dist = px.histogram(
        df, 
        x='numeric_price',
        title="Price Distribution",
        labels={'numeric_price': 'Price (TL)'},
        height=400
    )
    
    # Price by star rating
    fig_price_star = px.box(
        df,
        x='star_rating',
        y='numeric_price',
        title="Price by Star Rating",
        labels={
            'star_rating': 'Star Rating',
            'numeric_price': 'Price (TL)'
        },
        height=400
    )
    
    return fig_price_dist, fig_price_star

# Create review analysis visualizations
def create_review_analysis(df):
    # Review score distribution
    fig_score_dist = px.histogram(
        df, 
        x='numeric_review_score',
        title="Review Score Distribution",
        labels={'numeric_review_score': 'Review Score'},
        height=400
    )
    
    # Review score by star rating
    fig_score_star = px.box(
        df,
        x='star_rating',
        y='numeric_review_score',
        title="Review Score by Star Rating",
        labels={
            'star_rating': 'Star Rating',
            'numeric_review_score': 'Review Score'
        },
        height=400
    )
    
    return fig_score_dist, fig_score_star

# Create feature analysis visualizations
def create_feature_analysis(df):
    # Process features
    all_features = []
    feature_counts = {}
    
    for _, row in df.iterrows():
        features = row['features']
        if isinstance(features, list):
            for feature in features:
                all_features.append(feature)
                if feature in feature_counts:
                    feature_counts[feature] += 1
                else:
                    feature_counts[feature] = 1
    
    # Create feature frequency dataframe
    feature_df = pd.DataFrame({
        'feature': list(feature_counts.keys()),
        'count': list(feature_counts.values())
    }).sort_values('count', ascending=False)
    
    # Feature frequency chart
    fig_feature_freq = px.bar(
        feature_df,
        x='count',
        y='feature',
        orientation='h',
        title="Most Common Features",
        height=500
    )
    
    # Feature impact on review scores
    # Create a more meaningful feature impact analysis
    top_features = feature_df['feature'].head(5).tolist()
    
    # Prepare data for feature impact analysis
    impact_data = []
    
    for feature in top_features:
        # Hotels with this feature
        hotels_with_feature = []
        hotels_without_feature = []
        
        for _, row in df.iterrows():
            if isinstance(row['features'], list) and feature in row['features']:
                hotels_with_feature.append({
                    'review_score': row['numeric_review_score'],
                    'price': row['numeric_price']
                })
            else:
                hotels_without_feature.append({
                    'review_score': row['numeric_review_score'],
                    'price': row['numeric_price']
                })
        
        # Calculate averages
        if hotels_with_feature:
            avg_score_with = sum(h['review_score'] for h in hotels_with_feature) / len(hotels_with_feature)
            avg_price_with = sum(h['price'] for h in hotels_with_feature) / len(hotels_with_feature)
        else:
            avg_score_with = 0
            avg_price_with = 0
            
        if hotels_without_feature:
            avg_score_without = sum(h['review_score'] for h in hotels_without_feature) / len(hotels_without_feature)
            avg_price_without = sum(h['price'] for h in hotels_without_feature) / len(hotels_without_feature)
        else:
            avg_score_without = 0
            avg_price_without = 0
        
        impact_data.append({
            'feature': feature,
            'avg_score_with': avg_score_with,
            'avg_score_without': avg_score_without,
            'avg_price_with': avg_price_with,
            'avg_price_without': avg_price_without,
            'score_difference': avg_score_with - avg_score_without,
            'price_difference': avg_price_with - avg_price_without
        })
    
    impact_df = pd.DataFrame(impact_data)
    
    # Create feature impact visualization
    fig_feature_impact = go.Figure()
    
    for i, row in impact_df.iterrows():
        fig_feature_impact.add_trace(go.Bar(
            x=[row['feature']],
            y=[row['score_difference']],
            name=f"{row['feature']} (Score Impact)",
            marker_color='blue',
            text=f"Score diff: {row['score_difference']:.2f}",
            textposition='auto',
            offsetgroup=i
        ))
    
    fig_feature_impact.update_layout(
        title="Feature Impact on Review Scores",
        xaxis_title="Feature",
        yaxis_title="Score Difference (With vs Without Feature)",
        height=500,
        showlegend=False
    )
    
    return fig_feature_freq, fig_feature_impact

# Create location analysis visualizations
def create_location_analysis(df):
    # Location distribution
    location_counts = df['location'].value_counts().reset_index()
    location_counts.columns = ['location', 'count']
    
    fig_location = px.bar(
        location_counts,
        x='count',
        y='location',
        orientation='h',
        title="Hotels by Location",
        height=500
    )
    
    # Distance to center analysis
    # Filter out rows with missing distance_to_center
    distance_df = df[df['distance_to_center'].notna()].copy()
    
    # Extract numeric distance values
    def extract_distance(distance_str):
        if not distance_str or not isinstance(distance_str, str):
            return None
        
        match = re.search(r'(\d+\.?\d*)', distance_str)
        if match:
            return float(match.group(1))
        return None
    
    distance_df['numeric_distance'] = distance_df['distance_to_center'].apply(extract_distance)
    
    # Create scatter plot of distance vs price
    fig_distance = px.scatter(
        distance_df,
        x='numeric_distance',
        y='numeric_price',
        color='numeric_review_score',
        hover_name='name',
        title="Distance to Center vs. Price",
        labels={
            'numeric_distance': 'Distance to Center (km)',
            'numeric_price': 'Price (TL)',
            'numeric_review_score': 'Review Score'
        },
        height=500
    )
    
    return fig_location, fig_distance

# Main function
def main():
    # Page config
    st.set_page_config(
        page_title="Hotel Value Analysis Dashboard",
        page_icon="🏨",
        layout="wide"
    )
    
    # Header
    st.title("Hotel Value Analysis Dashboard")
    st.markdown("Interactive analysis of top value hotels")
    
    # Sidebar controls
    st.sidebar.header("Dashboard Controls")
    top_n = st.sidebar.slider("Number of Top Hotels", 5, 100, 10, 5)
    
    # Load data
    df = load_and_process_data('top_value_hotels.json', top_n)
    
    # Display summary metrics
    st.sidebar.subheader("Summary Statistics")
    st.sidebar.metric("Average Price", f"{df['numeric_price'].mean():.2f} TL")
    st.sidebar.metric("Average Review Score", f"{df['numeric_review_score'].mean():.2f}")
    st.sidebar.metric("Average Value Ratio", f"{df['value_ratio'].mean():.2f}")
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Value Overview", 
        "Price Analysis", 
        "Review Analysis", 
        "Feature Analysis", 
        "Location Analysis"
    ])
    
    # Tab 1: Value Overview
    with tab1:
        st.header("Value Ratio Analysis")
        
        # Create value overview visualizations
        fig_value, fig_scatter = create_value_overview(df)
        
        # Display visualizations in two columns
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_value, use_container_width=True)
        with col2:
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Display top hotels table
        st.subheader(f"Top {top_n} Hotels by Value Ratio")
        st.dataframe(
            df[['name', 'value_ratio', 'price', 'review_score', 'star_rating', 'location']]
        )
    
    # Tab 2: Price Analysis
    with tab2:
        st.header("Price Analysis")
        
        # Create price analysis visualizations
        fig_price_dist, fig_price_star = create_price_analysis(df)
        
        # Display visualizations
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_price_dist, use_container_width=True)
        with col2:
            st.plotly_chart(fig_price_star, use_container_width=True)
    
    # Tab 3: Review Analysis
    with tab3:
        st.header("Review Score Analysis")
        
        # Create review analysis visualizations
        fig_score_dist, fig_score_star = create_review_analysis(df)
        
        # Display visualizations
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_score_dist, use_container_width=True)
        with col2:
            st.plotly_chart(fig_score_star, use_container_width=True)
    
    # Tab 4: Feature Analysis
    with tab4:
        st.header("Feature Analysis")
        
        # Create feature analysis visualizations
        fig_feature_freq, fig_feature_impact = create_feature_analysis(df)
        
        # Display visualizations
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_feature_freq, use_container_width=True)
        with col2:
            st.plotly_chart(fig_feature_impact, use_container_width=True)
    
    # Tab 5: Location Analysis
    with tab5:
        st.header("Location Analysis")
        
        # Create location analysis visualizations
        fig_location, fig_distance = create_location_analysis(df)
        
        # Display visualizations
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_location, use_container_width=True)
        with col2:
            st.plotly_chart(fig_distance, use_container_width=True)

if __name__ == "__main__":
    main()
