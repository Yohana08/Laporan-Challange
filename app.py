import re
import pandas as pd

from flask import Flask, jsonify

app = Flask(__name__)

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
    'version': LazyString(lambda: '1.0.0'),
    'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,             
                  config=swagger_config)

@swag_from("docs/hello_world.yml", methods=['GET'])
@app.route('/', methods=['GET'])
def hello_world():
    json_response = {
        'status_code': 200,
        'description': "Menyapa Hello World",
        'data': "Hello World",
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text.yml", methods=['GET'])
@app.route('/text', methods=['GET'])
def text():
    json_response = {
        'status_code': 200,
        'description': "Original Teks",
        'data': "Halo, apa kabar semua?",
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text_clean.yml", methods=['GET'])
@app.route('/text-clean', methods=['GET'])
def text_clean():
    json_response = {
        'status_code': 200,
        'description': "Teks bersih",
        'data': re.sub(r'[^a-zA-Z0-9]', ' ', "Halo, apa kabar semua?"),
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():

    text = request.form.get('text')

    json_response = {
        'status_code': 200,
        'description': "Teks yang akan diproses",
        'data': re.sub(r'[0-9]', ' ', text).replace('\n', ' ').replace('rt', ' ').replace('USER', ' ').replace(r'((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', ' ').replace('  +', ' ').lower(),

        # re.sub('\n',' ',text)  Remove every '\n'
        # re.sub('rt',' ',text) Remove every retweet symbol
        # re.sub('user',' ',text)  Remove every username
        # re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text)  Remove every URL
        # re.sub('  +', ' ', text)  Remove extra spaces

    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text_processing_file.yml", methods=['POST'])
@app.route('/text-processing-file', methods=['POST'])
def text_processing_file():

    # Upladed file
    file = request.files.getlist('file')[0]

    # Import file csv ke Pandas
    df = pd.read_csv(file)
    assert df.coloums == 'text'

    # Ambil teks yang akan diproses dalam format list
    texts = df.text.to_list()

    # Lakukan cleansing pada teks
    cleaned_text = []
    for text in texts:
        cleaned = re.sub(r"[^a-zA-Z0-9]", "", text).replace('\n', ' ').replace('rt', ' ').replace('user', ' ').replace(r'((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', ' ').replace('  +', ' ').lower()
        cleaned_text.append(cleaned)

        # re.sub('\n',' ',text)  Remove every '\n'
        # re.sub('rt',' ',text) Remove every retweet symbol
        # re.sub('user',' ',text)  Remove every username
        # re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text)  Remove every URL
        # re.sub('  +', ' ', text)  Remove extra spaces

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': cleaned_text,
    }

    return jsonify(json_response)
    

if __name__ == '__main__':
   app.run()

