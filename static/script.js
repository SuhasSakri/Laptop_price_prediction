// Load options on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadOptions();
});

// Load dropdown options
async function loadOptions() {
    try {
        const response = await fetch('/api/options');
        const data = await response.json();
        
        // Populate brand dropdowns
        const predictBrand = document.getElementById('predict-brand');
        const recommendBrand = document.getElementById('recommend-brand');
        
        data.brands.forEach(brand => {
            predictBrand.innerHTML += `<option value="${brand}">${brand}</option>`;
            recommendBrand.innerHTML += `<option value="${brand}">${brand}</option>`;
        });
        
        // Populate OS dropdown
        const predictOS = document.getElementById('predict-os');
        data.os.forEach(os => {
            predictOS.innerHTML += `<option value="${os}">${os}</option>`;
        });
        
        // Populate processor dropdown
        const predictProcessor = document.getElementById('predict-processor');
        data.processors.forEach(processor => {
            predictProcessor.innerHTML += `<option value="${processor}">${processor}</option>`;
        });
    } catch (error) {
        console.error('Error loading options:', error);
    }
}

// Tab switching
function showTab(tabName) {
    const tabs = document.querySelectorAll('.tab-content');
    const buttons = document.querySelectorAll('.tab-btn');
    
    tabs.forEach(tab => tab.classList.remove('active'));
    buttons.forEach(btn => btn.classList.remove('active'));
    
    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.target.classList.add('active');
}

// Price Prediction Form
document.getElementById('predict-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        brand: document.getElementById('predict-brand').value,
        os: document.getElementById('predict-os').value,
        processor: document.getElementById('predict-processor').value,
        ram: document.getElementById('predict-ram').value,
        storage: document.getElementById('predict-storage').value,
        screen_size: document.getElementById('predict-screen').value,
        specs_score: document.getElementById('predict-specs').value
    };
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('predicted-price').textContent = 
                data.predicted_price.toLocaleString('en-IN');
            document.getElementById('prediction-result').style.display = 'block';
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error making prediction: ' + error.message);
    }
});

// Recommendations Form
document.getElementById('recommend-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        budget: document.getElementById('budget').value,
        brand: document.getElementById('recommend-brand').value,
        min_ram: document.getElementById('min-ram').value,
        min_storage: document.getElementById('min-storage').value
    };
    
    const resultsDiv = document.getElementById('recommendations-result');
    resultsDiv.innerHTML = '<div class="loading">🔍 Finding best laptops for you...</div>';
    
    try {
        const response = await fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayRecommendations(data.recommendations);
        } else {
            resultsDiv.innerHTML = `<div class="error">Error: ${data.error}</div>`;
        }
    } catch (error) {
        resultsDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
});

// Display recommendations
function displayRecommendations(laptops) {
    const resultsDiv = document.getElementById('recommendations-result');
    
    if (laptops.length === 0) {
        resultsDiv.innerHTML = '<div class="loading">No laptops found matching your criteria.</div>';
        return;
    }
    
    resultsDiv.innerHTML = laptops.map(laptop => `
        <div class="laptop-card">
            <img src="${laptop.image_url}" alt="${laptop.name}" class="laptop-image" 
                 onerror="this.src='https://via.placeholder.com/300x200?text=No+Image'">
            <div class="laptop-name">${laptop.name}</div>
            <div class="laptop-price">₹${laptop.price.toLocaleString('en-IN')}</div>
            <div class="laptop-specs">
                <strong>Brand:</strong> ${laptop.brand}<br>
                <strong>Processor:</strong> ${laptop.processor}<br>
                <strong>RAM:</strong> ${laptop.ram}<br>
                <strong>Storage:</strong> ${laptop.storage}<br>
                <strong>Graphics:</strong> ${laptop.graphics}<br>
                <strong>Screen:</strong> ${laptop.screen_size}
            </div>
            <span class="laptop-rating">⭐ ${laptop.ratings}</span>
        </div>
    `).join('');
}
