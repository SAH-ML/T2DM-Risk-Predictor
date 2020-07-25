from flask import Flask, render_template, request, jsonify
import mimetypes
import requests
import os
from flask_cors import CORS, cross_origin
mimetypes.add_type("text/css", ".css", True)
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST']) # To render Homepage
def home_page():
    return render_template('index.html')

@app.route('/diabetes', methods=['POST'])  # This will be called from UI
def diabetes_prediction():
    if (request.method=='POST'):
        region = int(request.form['region'])
        gender = int(request.form['gender'])
        bmi = int(request.form['bmi'])
        diet = int(request.form['diet'])
        bp = int(request.form['bp'])
        smoking = int(request.form['smoking'])

        url = "https://ussouthcentral.services.azureml.net/workspaces/ff3b958f513142458fdbe2c36d2d9072/services/93bd10dc4b0f4d0696e49b9efacc6ae1/execute?api-version=2.0&format=swagger"

        payload = "{\r\n        \"Inputs\": {\r\n                \"input1\":\r\n                [\r\n                    {\r\n                            'Regions': \""+ str(region) +"\",   \r\n                            'Gender': \""+ str(gender) +"\",   \r\n                            'BMI': \""+ str(bmi) +"\",   \r\n                            'Diet': \""+ str(diet) +"\",   \r\n                            'BP': \""+ str(bp) +"\",   \r\n                            'Smoking': \""+ str(smoking) +"\",   \r\n                    }\r\n                ],\r\n        },\r\n    \"GlobalParameters\":  {\r\n    }\r\n}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer yF1e0kPpKInrCJsvzXJ1oatt6NLkom6a0dov5b8zSDBdiH8t4UiTsg7MXtdbtlEPOb0IY0WDspCVnwVbX19RHQ=='
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        result = response.text[60:80]
        result +=" and           "
        result +=response.text[82:123]
        return render_template('results.html', result=result)



port = int(os.getenv("PORT"))
if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=port)
