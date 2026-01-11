import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# Page config
st.set_page_config(
    page_title="Laptop Price Predictor", 
    page_icon="💻", 
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "Laptop Price Predictor using Machine Learning"
    }
)

# Custom CSS for styling
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('laptops.csv')
    return df

@st.cache_resource
def train_model(df):
    data = df.copy()
    data['ram_gb'] = data['ram'].str.extract(r'(\d+)').astype(float)
    data['storage_gb'] = data['storage'].str.extract(r'(\d+)').astype(float)
    data['screen_size_num'] = data['screen_size'].str.extract(r'(\d+\.?\d*)').astype(float)
    
    le_brand = LabelEncoder()
    le_os = LabelEncoder()
    le_processor = LabelEncoder()
    
    data['brand_encoded'] = le_brand.fit_transform(data['brand'])
    data['os_encoded'] = le_os.fit_transform(data['os'].fillna('Unknown'))
    data['processor_encoded'] = le_processor.fit_transform(data['processor'].fillna('Unknown'))
    
    features = ['brand_encoded', 'os_encoded', 'processor_encoded', 'ram_gb', 
                'storage_gb', 'screen_size_num', 'specs_score']
    
    X = data[features].fillna(0)
    y = data['price']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model, le_brand, le_os, le_processor

df = load_data()
model, le_brand, le_os, le_processor = train_model(df)

# Header
st.title("💻 Laptop Price Predictor & Recommender")
st.markdown("---")

# Tabs
tab1, tab2 = st.tabs(["🔮 Price Prediction", "🎯 Recommendations"])

# TAB 1: Price Prediction
with tab1:
    st.header("Predict Laptop Price")
    
    col1, col2 = st.columns(2)
    
    with col1:
        brand = st.selectbox("Brand", sorted(df['brand'].unique()))
        os = st.selectbox("Operating System", sorted(df['os'].dropna().unique()))
        processor = st.selectbox("Processor", sorted(df['processor'].dropna().unique())[:50])
    
    with col2:
        ram = st.number_input("RAM (GB)", min_value=4, max_value=128, value=8)
        storage = st.number_input("Storage (GB)", min_value=128, max_value=4096, value=512)
        screen_size = st.number_input("Screen Size (inches)", min_value=11.0, max_value=18.0, value=15.6, step=0.1)
    
    specs_score = st.slider("Specs Score", 0, 100, 60)
    
    if st.button("🔮 Predict Price", type="primary"):
        try:
            brand_encoded = le_brand.transform([brand])[0]
            os_encoded = le_os.transform([os])[0]
            processor_encoded = le_processor.transform([processor])[0]
            
            features = np.array([[brand_encoded, os_encoded, processor_encoded, 
                                ram, storage, screen_size, specs_score]])
            
            prediction = model.predict(features)[0]
            
            st.success(f"### Predicted Price: ₹{prediction:,.2f}")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

# TAB 2: Recommendations
with tab2:
    st.header("Find Your Perfect Laptop")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        budget = st.number_input("Budget (₹)", min_value=10000, max_value=1000000, value=50000, step=5000)
    
    with col2:
        brand_filter = st.selectbox("Preferred Brand", ["Any"] + sorted(df['brand'].unique()))
    
    with col3:
        min_ram = st.number_input("Minimum RAM (GB)", min_value=0, max_value=128, value=8)
    
    min_storage = st.number_input("Minimum Storage (GB)", min_value=0, max_value=4096, value=256)
    
    if st.button("🎯 Get Recommendations", type="primary"):
        filtered = df.copy()
        filtered['ram_gb'] = filtered['ram'].str.extract(r'(\d+)').astype(float)
        filtered['storage_gb'] = filtered['storage'].str.extract(r'(\d+)').astype(float)
        
        filtered = filtered[filtered['price'] <= budget * 1.1]
        if brand_filter != "Any":
            filtered = filtered[filtered['brand'] == brand_filter]
        filtered = filtered[filtered['ram_gb'] >= min_ram]
        filtered = filtered[filtered['storage_gb'] >= min_storage]
        
        filtered['value_score'] = filtered['specs_score'] / (filtered['price'] / 10000)
        filtered = filtered.sort_values('value_score', ascending=False).head(10)
        
        if len(filtered) == 0:
            st.warning("No laptops found matching your criteria. Try adjusting filters.")
        else:
            st.success(f"Found {len(filtered)} laptops for you!")
            
            for idx, row in filtered.iterrows():
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        st.image(row['image_url'], width=200)
                    
                    with col2:
                        st.subheader(row['name'][:80])
                        st.markdown(f"### ₹{row['price']:,.0f}")
                        st.markdown(f"⭐ **Rating:** {row['ratings']}")
                        st.markdown(f"**Processor:** {row['processor']}")
                        st.markdown(f"**RAM:** {row['ram']} | **Storage:** {row['storage']}")
                        st.markdown(f"**Graphics:** {row['graphics']}")
                        st.markdown(f"**Screen:** {row['screen_size']}")
                    
                    st.markdown("---")
