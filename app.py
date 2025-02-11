# Dependencies
import sys
import traceback
import joblib
import pandas as pd
from flask import Flask, request, jsonify
import os

# API definition
app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    currentAbsolutePath = os.path.dirname(os.path.abspath(__file__))

    modelPath = currentAbsolutePath + '/machine_learning_files/model.pkl'

    model = joblib.load(modelPath)  # Load model.pkl
    print('Model loaded')

    modelColumnsPath = currentAbsolutePath + '/machine_learning_files/model_columns.pkl'

    model_columns = joblib.load(modelColumnsPath)  # Load model_columns.pkl
    print('Model columns loaded')

    if model:
        try:
            json_ = request.json
            print(json_)
            query = pd.get_dummies(pd.DataFrame(json_))
            query = query.reindex(columns=model_columns, fill_value=0)

            prediction = list(model.predict(query))

            return jsonify({'prediction': str(prediction)})

        except:

            return jsonify({'trace': traceback.format_exc})

    else:

        print('train the model first')
        return 'no model here to use'


if __name__ == '__main__':
    # try:
    #     port = int(sys.argv[1])  # This is for a command line input
    # except:
    #     port = 3000  # if you don't provide any port the port will be set to 1

    # @app.before_first_request
    # def load_machine_learning_models():
    #     currentAbsolutePath = os.path.dirname(os.path.abspath(__file__))
    #
    #     modelPath = currentAbsolutePath + '/machine_learning_files/model.pkl'
    #
    #     model = joblib.load(modelPath)  # Load model.pkl
    #     print('Model loaded')
    #
    #     modelColumnsPath = currentAbsolutePath + '/machine_learning_files/model_columns.pkl'
    #
    #     model_columns = joblib.load(modelColumnsPath)  # Load model_columns.pkl
    #     print('Model columns loaded')

    print('API Starting...')
    app.run(port=3000, debug=True)
