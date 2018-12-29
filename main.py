# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
from flask import Response
from flask import send_from_directory
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('.', 'favicon.ico')

@app.route('/logo.png')
def logo():
    return send_from_directory('.', 'logo.png')

@app.route('/dnt-policy.txt')
def dnt():
    return send_from_directory('.', 'dnt-policy.txt')

@app.route('/formula')
def formula():
    return send_from_directory('.', 'formula.html')

@app.route('/oEmbed')
def embed():
    required_tags = ['formula', 'height', 'width']
    url = request.args.get('url')
    parsed_url = urlparse(url)
    query_string = parsed_url[4]
    query = parse_qs(query_string)
    missing_tags = list(filter(lambda x: x not in query, required_tags))
    if missing_tags:
        return ('These keys of the query are required: {}'.format(
            ', '.join(missing_tags)), 404)

    height = query['height'][0]
    width = query['width'][0]
    rspns = {
        'type': 'rich',
        'version': '1.0',
        'provider_name': 'Formula Embed',
        'provider_url': parsed_url[1],
        'html': '<iframe width="{}" height="{}" scrolling="no" ' \
            'frameborder="no" src="{}"></iframe>'.format(width, height, url),
        'width': width,
        'height': height
    }
    
    return Response(json.dumps(rspns), mimetype='application/json') 


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
