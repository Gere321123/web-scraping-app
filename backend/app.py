from flask import Flask, request, jsonify
from flask_cors import CORS
import concurrent.futures
import logging
from ddor_travel import get_travel_price_ddor
from sava_travel import get_travel_price_sava
from e_tigrav_travel import get_travel_price_etigrav

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/api', methods=['POST'])
def get_data():
    data = request.json
    arrival_date = data.get('arrivalDate')
    departure_date = data.get('departureDate')
    ages = data.get('ages')
    sport = data.get('sport')

    response_data = {}
    
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # future_ddor = executor.submit(get_travel_price_ddor, arrival_date, departure_date, ages, sport)
            # future_sava = executor.submit(get_travel_price_sava, arrival_date, departure_date, ages)
            future_etigrav = executor.submit(get_travel_price_etigrav, arrival_date, departure_date, ages)
            

        sava_price = future_sava.result()
        ddor_price = future_ddor.result()
            
        response_data = {
            'ddor_price': ddor_price,
            'sava_price': sava_price
        }
        app.logger.info(f"Response data: {response_data}")
            
    except Exception as e:
        response_data = {'error': str(e)}
        app.logger.error(f"Error: {e}")

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
