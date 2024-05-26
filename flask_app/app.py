from flask import Flask, request, jsonify
import pickle
import numpy as np
import json

app = Flask(__name__)

# Load the model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the example query
with open('example_query.json', 'r') as f:
    example_query = json.load(f)
    
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # Convert JSON input to DataFrame
    input_data = np.array(data['history']).reshape(1, -1)
    prediction = model.predict(input_data)
    return jsonify({'prediction': prediction[0]})

@app.route('/example_query', methods=['GET'])
def get_example_query():
    input_data = np.array(example_query['history']).reshape(1, -1)
    prediction = model.predict(input_data)
    return jsonify({"prediction": prediction[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
