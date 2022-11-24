from flask import Flask,jsonify,request,Response
from flask_httpauth import HTTPBasicAuth
from prometheus_flask_exporter import PrometheusMetrics
import requests
from requests.adapters import HTTPAdapter, Retry
import os
import json



# init flask
app =   Flask(__name__)

# init auth
auth = HTTPBasicAuth()

# init metrics
metrics = PrometheusMetrics(app,metrics_decorator=auth.login_required)

# Metric app version
metrics.info('app_version', 'Application version', version='0.0.1')

# auth settings for metrics
@auth.verify_password
def verify_credentials(username, password):
    return (username, password) == ('metrics', 'metrics')

  
@app.route('/weather/<city>', methods = ['GET'])
@metrics.summary('requests_by_status', 'Request latencies by status', labels={'status': lambda r: r.status_code})
@metrics.counter(
    'response_by_status', 'Request Count by status', labels={
        'status': lambda resp: resp.status_code
    })
def ReturnJSON(city):
    
    api = os.getenv('WEATHER_API')
    url = "http://api.openweathermap.org/data/2.5/weather?"+ "appid=" + api + "&q=" + city
    
    try:
        s = requests.Session()
        retries = Retry(total=3,
                        backoff_factor=1,
                        status_forcelist=[429, 500, 502, 503, 504],
                        method_whitelist=["HEAD", "GET", "OPTIONS"])

        s.mount('http://', HTTPAdapter(max_retries=retries))

        data = s.get(url)
        
        if(data.status_code == 404):
            return data.content.decode('utf-8'), 404, {"Content-type": "application/json; charset=utf-8"}
        
        return data.content.decode('utf-8'), 200, {"Content-type": "application/json; charset=utf-8"}
        
    except Exception as e:
        return jsonify(str(e)), 500, {"Content-type": "application/json; charset=utf-8"}      
    
@app.route('/', methods = ['GET'])
def main():
    data = {
        "ping": "pong"
    }
  
    return jsonify(data)