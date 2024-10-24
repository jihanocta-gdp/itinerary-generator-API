import openai
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from

# Masukkan API Key langsung di kode
OPENAI_API_KEY = "place your API key"  # Replace with your real API key
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/api/places', methods=['POST'])
@swag_from({
    'tags': ['Places'],
    'description': 'Mengambil daftar tempat wisata di negara tertentu.',
    'parameters': [
        {
            'name': 'country',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'country': {'type': 'string', 'example': 'Japan'}
                },
            },
        }
    ],
    'responses': {
        200: {
            'description': 'Daftar tempat wisata.',
            'schema': {
                'type': 'array',
                'items': {'type': 'string'}
            }
        },
        400: {'description': 'Invalid or missing country name.'}
    }
})
def get_places():
    data = request.get_json()

    try:
        country = data['country']

        # Generate a list of places to visit using OpenAI
        prompt = f"List the top places to visit in {country}."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that provides travel recommendations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        places = response.choices[0].message['content'].strip()

        # Return the list of places as an array
        return jsonify({"places_to_visit": places.split('\n')}), 200

    except KeyError:
        return jsonify({"error": "Missing 'country' field in request body."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
