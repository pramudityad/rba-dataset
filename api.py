# api.py
from flask import Flask, request, jsonify
import joblib
import numpy as np
from flasgger import Swagger
from mock_fhir import MockFHIRClient  # Import the mock FHIR client

app = Flask(__name__)
swagger = Swagger(app)

# Load the trained model from the pickle file
model = joblib.load('./rfc_model_pkl')

# Initialize the mock FHIR client
fhir_client = MockFHIRClient()

@app.route('/')
def index():
    return "Random Forest API is up and running!"

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict using Random Forest Model
    ---
    tags:
      - Prediction
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - features
            - patient_id
          properties:
            features:
              type: array
              items:
                type: number
              example: [5.1, 3.5, 1.4, 0.2]
            patient_id:
              type: string
              example: "example_patient_id"
    responses:
      200:
        description: Prediction result
        schema:
          type: object
          properties:
            prediction:
              type: integer
              example: 1
            observation:
              type: object
      400:
        description: Bad Request
        schema:
          type: object
          properties:
            error:
              type: string
              example: Missing features key in the JSON data
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: Internal error message
    """
    if request.method == 'POST':
        try:
            # Get the JSON from the request
            data = request.get_json()

            # Ensure the 'features' key is in the incoming JSON data
            if 'features' not in data:
                return jsonify({'error': 'Missing features key in the JSON data'}), 400

            # Ensure the 'patient_id' key is in the incoming JSON data
            if 'patient_id' not in data:
                return jsonify({'error': 'Missing patient_id key in the JSON data'}), 400

            # Extract patient ID
            patient_id = data['patient_id']

            # Convert data into a numpy array
            input_features = np.array(data['features']).reshape(1, -1)
            
            # Make a prediction
            prediction = model.predict(input_features)
            if prediction[0] == 0:
                return jsonify({'error': 'User not authorized'}), 401

            # Store prediction result as an Observation
            observation_result = fhir_client.get_patient(patient_id)

            # Send the response back to the client
            return jsonify({
                'prediction': int(prediction[0]),
                'observation': observation_result
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)