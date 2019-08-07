from requests import post, get
from flask import Flask, request, redirect, url_for, flash, make_response
from flask_cors import CORS
from config import CONFIG as config
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_URL=os.getenv("CRM_API_URL")

app = Flask(__name__)
app.config['CONFIG'] = config
CORS(app)


def get_business_access(headers, businessId = None):
    print(app.config)
    if not businessId is None and len(businessId) > 0:
        url = f'{API_URL}/business?id=eq.{businessId}'
        print(url)
        try:
          res = get(url, headers={'Authorization':headers['Authorization']}, timeout=3)
          j = res.json()
          print(j)
          if j is None:
            return False
          return j[0]['access'] == True
        except KeyError:
          pass
        except IndexError:
          pass
    return False


@app.route('/business/<businessId>', methods=['GET'])
def business_access(businessId):
    print(request.method)
    print(request.headers)
    res = get_business_access(headers = request.headers, businessId = businessId)
    return make_response(json.dumps({'access': res}), 200, {'Content-Type': 'application/json'})


@app.route('/', methods=['GET', 'POST'])
def root_route():
    print(request.method)
    print(request.headers)
    if request.method == 'POST':
      return redirect(request.url)

    return '''
    <!doctype html>
Auth service
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0')
