from requests import post, get
from flask import Flask, request, redirect, url_for, flash, make_response
from flask_cors import CORS
import json
from dotenv import load_dotenv
import os
import logging


load_dotenv()

API_URL=os.getenv("API_URL")

app = Flask(__name__)
CORS(app)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)


def get_business_access(headers, businessId = None):
    if not businessId is None and len(businessId) > 0:
        url = f'{API_URL}/business?id=eq.{businessId}'
        try:
          res = get(url, headers={'Authorization':headers['Authorization']}, timeout=3)
          j = res.json()
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
    app.logger.debug(f"{request.method} {request.headers}")
    res = get_business_access(headers = request.headers, businessId = businessId)
    return make_response(json.dumps({'access': res}), 200, {'Content-Type': 'application/json'})


@app.route('/', methods=['GET', 'POST'])
def root_route():
    app.logger.debug(f"{request.method} {request.headers}")
    if request.method == 'POST':
      return redirect(request.url)

    return '''
    <!doctype html>
Auth service
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0')
