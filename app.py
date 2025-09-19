from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
from utils.chatbot_logic import generate_chatbot_response

app = Flask(__name__)

# Load models and encoders
model = joblib.load("model/crop_model.pkl")
scaler = joblib.load("model/scaler.pkl")
label_encoders = joblib.load("model/label_encoders.pkl")
target_encoder = joblib.load("model/target_encoder.pkl")  # For decoding label (crop name)

# Default values for optional fields
DEFAULTS = {
    "sunlight_hours": 8.0
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("About.html")

@app.route('/instructions')
def instructions():
    return render_template("instructions.html")

@app.route('/webpage')
def webpage():
    return render_template("webpage.html")

@app.route('/predict', methods=['POST'])
def predict_crop():
    try:
        data = request.json

        # Required numerical fields
        numerical_fields = [
            "N", "P", "K", "temperature", "humidity",
            "ph", "rainfall", "water_availability", "sunlight_hours"
        ]

        numerical_features = []
        for field in numerical_fields:
            value = data.get(field, DEFAULTS.get(field))
            if value is None:
                return jsonify({"error": f"Missing field: {field}"}), 400
            try:
                numerical_features.append(float(value))
            except ValueError:
                return jsonify({"error": f"Invalid value for {field}: {value}"}), 400

        # Categorical fields
        categorical_fields = ['season', 'district', 'soil_type', 'fertilizer_used']
        encoded_cats = []

        for col in categorical_fields:
            le = label_encoders.get(col)
            if le is None:
                return jsonify({"error": f"Label encoder missing for {col}"}), 500
            value = data.get(col)
            if value is None:
                return jsonify({"error": f"Missing field: {col}"}), 400
            try:
                encoded_value = int(le.transform([value])[0])
            except ValueError:
                return jsonify({"error": f"Unknown value for {col}: {value}"}), 400
            encoded_cats.append(encoded_value)

        # Prepare final input
        final_input = np.array(numerical_features + encoded_cats).reshape(1, -1)
        final_input_scaled = scaler.transform(final_input)

        prediction = model.predict(final_input_scaled)[0]
        predicted_crop = target_encoder.inverse_transform([prediction])[0]

        return jsonify({"predicted_crop": str(predicted_crop)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chatbot_reply():
    try:
        user_msg = request.json.get('message')
        if not user_msg:
            return jsonify({"response": "Please enter a message."})

        response = generate_chatbot_response(user_msg)
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500
@app.context_processor
def inject_encoder_options():
    # Get the valid classes for each categorical field
    options = {}
    for col in ['season', 'district', 'soil_type', 'fertilizer_used']:
        le = label_encoders.get(col)
        if le:
            # Convert to list of strings
            options[col] = le.classes_.tolist()
    return dict(encoder_options=options)


if __name__ == '__main__':
    app.run(debug=True)
