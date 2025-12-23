%%writefile app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns

st.set_page_config(page_title="Data Explorer Dashboard", layout="wide")

st.title("📊 Interactive Data Explorer")
st.markdown("Upload any CSV file and explore it instantly!")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.success(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns!")
    
    # Tabs for organization
    tab1, tab2, tab3 = st.tabs(["📋 Data Preview", "📈 Visualizations", "📊 Statistics"])
    
    with tab1:
        st.subheader("First 10 Rows")
        st.dataframe(df.head(10))
        
        st.subheader("Full Dataset")
        st.dataframe(df)
    
    with tab2:
        st.subheader("Select columns to plot")
        
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("X-axis", df.columns)
        with col2:
            y_col = st.selectbox("Y-axis", df.columns, index=min(1, len(df.columns)-1))
        
        color_col = st.selectbox("Color by (optional)", ["None"] + list(df.columns))
        
        if color_col == "None":
            color_col = None
            
        fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                         title=f"{y_col} vs {x_col}")
        st.plotly_chart(fig, use_container_width=True)
        
        # Histogram
        hist_col = st.selectbox("Column for Histogram", df.select_dtypes(include='number').columns)
        fig_hist = px.histogram(df, x=hist_col, title=f"Distribution of {hist_col}")
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with tab3:
        st.subheader("Summary Statistics")
        st.dataframe(df.describe(include='all'))
        
        st.subheader("Missing Values")
        missing = df.isnull().sum()
        st.dataframe(missing[missing > 0])

else:
    st.info("👆 Upload a CSV file to begin exploration")
    st.markdown("Try with Titanic, Iris, or any business data!")
