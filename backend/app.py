from flask import Flask, request, jsonify
from flask_cors import CORS
from ddor_travel import get_travel_price

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['POST'])
def get_data():
    data = request.json
    arrival_date = data.get('arrivalDate')
    departure_date = data.get('departureDate')
    ages = data.get('ages')
    sport = data.get('sport')

    try:
        price = get_travel_price(arrival_date, departure_date, ages, sport)
        response_data = {'price': price}
    except Exception as e:
        response_data = {'error': str(e)}

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
