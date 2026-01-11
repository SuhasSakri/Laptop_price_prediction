from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import os

app = Flask(__name__)

# Load and prepare data
df = pd.read_csv('laptops.csv')

# Prepare features for ML model
def prepare_data():
    data = df.copy()
    
    # Extract numeric features
    data['ram_gb'] = data['ram'].str.extract(r'(\d+)').astype(float)
    data['storage_gb'] = data['storage'].str.extract(r'(\d+)').astype(float)
    data['screen_size_num'] = data['screen_size'].str.extract(r'(\d+\.?\d*)').astype(float)
    
    # Encode categorical features
    le_brand = LabelEncoder()
    le_os = LabelEncoder()
    le_processor = LabelEncoder()
    
    data['brand_encoded'] = le_brand.fit_transform(data['brand'])
    data['os_encoded'] = le_os.fit_transform(data['os'].fillna('Unknown'))
    data['processor_encoded'] = le_processor.fit_transform(data['processor'].fillna('Unknown'))
    
    # Select features
    features = ['brand_encoded', 'os_encoded', 'processor_encoded', 'ram_gb', 
                'storage_gb', 'screen_size_num', 'specs_score']
    
    X = data[features].fillna(0)
    y = data['price']
    
    return X, y, le_brand, le_os, le_processor

# Train model
X, y, le_brand, le_os, le_processor = prepare_data()
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save encoders
encoders = {
    'brand': le_brand,
    'os': le_os,
    'processor': le_processor
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Encode inputs
        brand_encoded = encoders['brand'].transform([data['brand']])[0]
        os_encoded = encoders['os'].transform([data['os']])[0]
        processor_encoded = encoders['processor'].transform([data['processor']])[0]
        
        # Prepare features
        features = np.array([[
            brand_encoded,
            os_encoded,
            processor_encoded,
            float(data['ram']),
            float(data['storage']),
            float(data['screen_size']),
            float(data.get('specs_score', 50))
        ]])
        
        # Predict
        prediction = model.predict(features)[0]
        
        return jsonify({
            'success': True,
            'predicted_price': round(prediction, 2)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        budget = float(data['budget'])
        brand = data.get('brand', None)
        min_ram = float(data.get('min_ram', 0))
        min_storage = float(data.get('min_storage', 0))
        
        # Filter laptops
        filtered = df.copy()
        filtered['ram_gb'] = filtered['ram'].str.extract(r'(\d+)').astype(float)
        filtered['storage_gb'] = filtered['storage'].str.extract(r'(\d+)').astype(float)
        
        # Apply filters
        filtered = filtered[filtered['price'] <= budget * 1.1]
        if brand and brand != 'Any':
            filtered = filtered[filtered['brand'] == brand]
        filtered = filtered[filtered['ram_gb'] >= min_ram]
        filtered = filtered[filtered['storage_gb'] >= min_storage]
        
        # Sort by value (specs_score / price ratio)
        filtered['value_score'] = filtered['specs_score'] / (filtered['price'] / 10000)
        filtered = filtered.sort_values('value_score', ascending=False).head(10)
        
        # Prepare response
        recommendations = []
        for _, row in filtered.iterrows():
            recommendations.append({
                'name': row['name'],
                'brand': row['brand'],
                'price': row['price'],
                'processor': row['processor'],
                'ram': row['ram'],
                'storage': row['storage'],
                'graphics': row['graphics'],
                'screen_size': row['screen_size'],
                'ratings': row['ratings'],
                'image_url': row['image_url']
            })
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/options')
def get_options():
    return jsonify({
        'brands': sorted(df['brand'].unique().tolist()),
        'os': sorted(df['os'].dropna().unique().tolist()),
        'processors': sorted(df['processor'].dropna().unique().tolist()[:50])
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
