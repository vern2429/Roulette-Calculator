import json
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Pi Network API Key and Wallet Address
PI_API_KEY = "91fjl06tqnangipkbihqmlfjlpaptktycpx03hhmxupyyctusn3wcwiwy3bzuhj9"
PI_WALLET_ADDRESS = "GCYXJHDUICM5J7GPLNJZIFY6Z3EPRDZAB2ABPOIBZ2Q53T6ZBSB3VX56"

# Define payout odds
PAYOUTS = {
    "straight": 35,
    "split": 17,
    "street": 11,
    "corner": 8,
    "sixLine": 5,
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        data = request.json
        total_payout = 0
        results = {}

        for bet_type, odds in PAYOUTS.items():
            chips = float(data.get(bet_type, 0))
            payout = chips * odds
            results[bet_type] = round(payout, 2)
            total_payout += payout

        return jsonify({"results": results, "total_payout": round(total_payout, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/start-payment", methods=["POST"])
def start_payment():
    try:
        data = request.json
        amount = float(data["amount"])
        metadata = {"message": "Donation to Roulette Calculator"}
        
        response = requests.post(
            "https://api.minepi.com/v2/payments",
            headers={"Authorization": f"Key {PI_API_KEY}"},
            json={
                "amount": amount,
                "memo": metadata,
                "metadata": json.dumps(metadata),
                "uid": "roulette_calculator_donation",
                "to_address": PI_WALLET_ADDRESS,
            }
        )
        
        payment_data = response.json()
        return jsonify(payment_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
