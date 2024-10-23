from flask import Flask, request, jsonify
from flask_cors import CORS
import main
import get_product_bot

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/start-bot', methods=['POST'])
def start_bot():
    data = request.get_json()

    profile_id = data['profileId']
    print(f"Profile ID: {profile_id}")
    main.run_bot(profile_id)

    return "Done"

@app.route('/get-product', methods=['POST'])
def get_product():
    data = request.get_json()

    location = data['location']
    sku = data['sku']
    print(f"Location: {location}    SKU: {sku}")

    product_data = get_product_bot.get_product(location, sku)

    return product_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
