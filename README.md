# 💻 Laptop Price Predictor & Recommender

A full-stack machine learning web application that predicts laptop prices and provides personalized laptop recommendations based on user specifications and budget.

## 🚀 Two Versions Available

### Flask Version (Full Control)
- Custom HTML/CSS/JS interface
- Complete control over design
- Production-ready
- RESTful API endpoints

### Streamlit Version (Quick & Simple)
- Auto-generated UI
- Minimal code
- Perfect for demos
- Rapid prototyping

## 🎯 Features

- **Price Prediction**: Predict laptop prices based on specifications using Random Forest ML model
- **Smart Recommendations**: Get personalized laptop suggestions based on budget and requirements
- **Interactive UI**: Modern, responsive web interface with real-time predictions
- **Comprehensive Dataset**: Uses real laptop data with prices, specs, and ratings

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🛠️ Installation

1. Navigate to the project directory:
```bash
cd laptop_prize_predictor
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Option 1: Flask Version

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and go to:
```
http://localhost:5000
```

### Option 2: Streamlit Version

1. Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

2. Browser opens automatically!

### Using the Application:
   - **Price Prediction Tab**: Enter laptop specifications to predict the price
   - **Recommendations Tab**: Set your budget and preferences to get laptop suggestions

## 📊 How It Works

### Machine Learning Model
- **Algorithm**: Random Forest Regressor
- **Features**: Brand, OS, Processor, RAM, Storage, Screen Size, Specs Score
- **Training**: Model is trained on real laptop data with 1000+ samples

### Price Prediction
1. User inputs laptop specifications
2. Features are encoded and normalized
3. ML model predicts the price
4. Result is displayed in INR

### Recommendations
1. User sets budget and minimum requirements
2. System filters laptops matching criteria
3. Laptops are ranked by value score (specs/price ratio)
4. Top 10 recommendations are displayed with images and details

## 🏗️ Project Structure

```
laptop_prize_predictor/
│
├── app.py                 # Flask backend with ML model
├── streamlit_app.py       # Streamlit version (alternative)
├── laptops.csv           # Dataset with laptop information
├── requirements.txt      # Python dependencies
├── README.md            # This file
│
├── templates/
│   └── index.html       # Frontend HTML (Flask)
│
└── static/
    ├── style.css        # CSS styling (Flask)
    └── script.js        # JavaScript for interactivity (Flask)
```

## 🎨 Technologies Used

- **Backend**: Flask (Python) / Streamlit
- **Machine Learning**: scikit-learn, pandas, numpy
- **Frontend**: HTML5, CSS3, JavaScript (Flask) / Auto-generated (Streamlit)
- **Model**: Random Forest Regressor

## 📊 Choose Your Version

| Feature | Flask | Streamlit |
|---------|-------|----------|
| **Setup Time** | Medium | Fast |
| **Customization** | Full control | Limited |
| **Code Lines** | ~300 | ~120 |
| **Best For** | Production, custom UI | Demos, prototypes |
| **Learning Curve** | Moderate | Easy |

## 📈 Model Performance

The Random Forest model provides accurate price predictions by considering:
- Brand reputation
- Processor generation and type
- RAM capacity
- Storage size
- Screen specifications
- Overall specs score

## 🔧 Customization

You can customize the application by:
- Modifying the ML model in `app.py`
- Adjusting the UI in `templates/index.html` and `static/style.css`
- Adding more features to the prediction model
- Updating the dataset with new laptop data

## 📝 API Endpoints

- `GET /` - Main application page
- `POST /predict` - Predict laptop price
- `POST /recommend` - Get laptop recommendations
- `GET /api/options` - Get available brands, OS, and processors

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Created with ❤️ for laptop enthusiasts and budget-conscious buyers!
