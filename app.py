from flask import Flask, request, jsonify
import numpy as np
from twilio.rest import Client
import paho.mqtt.client as mqtt

app = Flask(__name__)

# Mock function for ARIMA prediction
def predict_wqi(year):
    return round(np.random.uniform(50, 100), 2)  # Simulate WQI

# Twilio Alert Function
def send_alert(message, phone="+1234567890"):
    account_sid = "YOUR_TWILIO_SID"
    auth_token = "YOUR_TWILIO_AUTH"
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=message,
        from_="+YOUR_TWILIO_NUMBER",
        to=phone
    )

# MQTT Anomaly Detection
def on_message(client, userdata, message):
    data = message.payload.decode()
    print(f"MQTT Message Received: {data}")

    if float(data) < 50:  # If WQI < 50, send alert
        send_alert(f"🚨 Water quality anomaly detected! WQI: {data}")

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect("test.mosquitto.org", 1883, 60)
mqtt_client.subscribe("water/quality")
mqtt_client.loop_start()

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    year = data.get("year", 2025)
    prediction = predict_wqi(year)
    return jsonify({"wqi_prediction": prediction})

if __name__ == "__main__":
    app.run(debug=True)
