from flask import Flask, request, jsonify, render_template
import joblib

app = Flask(__name__)

# Load the model
MODEL = joblib.load('golf_prediction.v1.0.pkl')
HTTP_BAD_REQUEST = 400

@app.route('/')
def index():
    error = None
    return render_template(
        'weather.html',
        outlook_data=[{'name':'Overcast'}, {'name':'Rainy'}, {'name':'Sunny'}],
        temperature_data=[{'name':'Cool'}, {'name':'Hot'}, {'name':'Mild'}],
        humidity_data=[{'name':'High'}, {'name':'Normal'}],
        windy_data=[{'name':'False'}, {'name':'True'}],
        error = error)

@app.route("/result" , methods=['GET', 'POST'])
def result():
    data = []
    error = None
    outlook_select = request.form.get('outlook_select')
    temperature_select = request.form.get('temperature_select')
    humidity_select = request.form.get('humidity_select')
    windy_select = request.form.get('windy_select')
    resp = predict(outlook_select, temperature_select, humidity_select, windy_select)
    if resp:
        if(resp.json['label'] == 'yes'):
            data.append("Weather is suitable for playing golf.")
        else:
            data.append("Weather is not suitable for playing golf.")
        data.append(outlook_select)
        data.append(temperature_select)
        data.append(humidity_select)
        data.append(windy_select)
    if len(data) != 1:
        error = 'Bad Response from Golf Prediction API'
    return render_template(
        'result.html',
        data=data,
        error=error)

def predict(outlook, temperature, humidity, windy):
    # Retrieve query parameters related to this request.
    features_order = ['Overcast', 'Rainy', 'Sunny', 'Cool', 'Hot', 'Mild', 'High', 'Normal', 'False', 'True']

    # Reject request that have bad or missing values.
    if (outlook is None or temperature is None
            or humidity is None or windy is None):
        # Provide the caller with feedback on why the record is unscorable.
        message = ('Missing or unacceptable values.'
                   'All values must be present and of type string.')
        response = jsonify(status='error', error_message=message)
        # Sets the status code to 400
        response.status_code = HTTP_BAD_REQUEST
        return response

    features = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    features[0][features_order.index(outlook)] = 1
    features[0][features_order.index(temperature)] = 1
    features[0][features_order.index(humidity)] = 1
    features[0][features_order.index(windy)] = 1

    label = MODEL.predict(features)
    # Create and send a response to the API caller
    return jsonify(status='complete', label=label[0])

if __name__ == '__main__':
    app.run(debug=True)

# go: http://127.0.0.1:5000/predict?outlook=sunny&temperature=hot&humidity=normal&windy=false