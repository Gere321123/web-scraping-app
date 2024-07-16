from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from ddor_travel import get_travel_price_ddor
from sava_travel import get_travel_price_sava

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
        sava_price =  get_travel_price_sava(arrival_date, departure_date, ages)
        print(sava_price)
        ddor_price =  get_travel_price_ddor(arrival_date, departure_date, ages, sport)
        print(ddor_price)
        response_data = {
            'ddor_price': ddor_price,
            'sava_price': sava_price
        }
        print(response_data)
        
    except Exception as e:
        response_data = {'error': str(e)}

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
