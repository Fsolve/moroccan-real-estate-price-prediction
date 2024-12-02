from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
import pandas as pd
app = Flask(__name__)
# Load the model
with open('model_abdo.pkl', 'rb') as f:
    model, numeric_features, categorical_features  = pickle.load(f)



def safe_division(a, b):
    return 0 if b == 0 else a / b

def validate_input(type_bien, superficie, chambres, salles_de_bain):
    if superficie < 52 or superficie > 5000:  # Based on min/max from stats
        return False, "Invalid surface area"
        
    if chambres < 1 or chambres > 15:  # Based on min/max from stats
        return False, "Invalid number of rooms"
        
    if salles_de_bain < 0 or salles_de_bain > 8:  # Based on min/max from stats
        return False, "Invalid number of bathrooms"
        
    # # Property type specific validations based on stats
    # if type_bien == 'appartement':
    #     if superficie > 200:  # Apartments usually smaller
    #         return False, "Surface area too large for apartment"
    # elif type_bien == 'Villa et Riad':
    #     if superficie < 100:  # Villas usually larger
    #         return False, "Surface area too small for villa"
    # elif type_bien == 'Maison et Villa':
    #     if superficie < 80:
    #         return False, "Surface area too small for house"
            
    return True, None

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    error_message = None
    
    if request.method == 'POST':
        try:
            # Get values from form
            chambres = int(request.form['chambres'])
            salles_de_bain = int(request.form['salles_de_bain'])
            superficie = float(request.form['superficie'])
            type_bien = request.form['type']
            ville = request.form['ville']
            
            # Validate input
            is_valid, error = validate_input(type_bien, superficie, chambres, salles_de_bain)
            if not is_valid:
                error_message = error
            else:
                # Calculate engineered features
                rooms_per_bath = safe_division(chambres, salles_de_bain)
                
                # Create input DataFrame
                input_data = pd.DataFrame({
                    'chambres': [chambres],
                    'salles_de_bain': [salles_de_bain],
                    'superficie en m²': [superficie],
                   
                    'rooms_per_bath': [rooms_per_bath],
                    'type': [type_bien],
                    'ville': [ville]
                })
                
                # Ensure correct column order
                input_data = input_data[numeric_features + categorical_features]
                
                # Make prediction
                pred = model.predict(input_data)
                prediction = np.expm1(pred)[0]
                
                # # Apply range limits based on property type
                # if type_bien == 'appartement':
                #     prediction = min(max(prediction, 300000), 4500000)
                # elif type_bien == 'Maison et Villa':
                #     prediction = min(max(prediction, 500000), 4500000)
                # elif type_bien == 'Villa et Riad':
                #     prediction = min(max(prediction, 1000000), 4500000)
                
                # # Round to nearest 10000
                # prediction = round(prediction / 10000) * 10000
                
        except Exception as e:
            error_message = f"Error in prediction: {str(e)}"
            print(error_message)
    
    # Get unique values for dropdowns
    types = ['appartement', 'Villa et Riad', 'Maison et Villa']
    villes = ['Casablanca', 'Marrakech', 'Tanger', 'Kénitra', 'Salé', 'Fès', 'Rabat',
              'Agadir', 'Meknès', 'Temara', 'Oujda'] 
    
    return render_template('index.html', 
                         prediction=prediction,
                         error_message=error_message,
                         types=types, 
                         villes=villes)

if __name__ == '__main__':
    app.run(debug=True)