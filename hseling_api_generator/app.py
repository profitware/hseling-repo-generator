from flask import Flask, request, Response, jsonify
from jsonrpc import JSONRPCResponseManager, dispatcher

import sample


app = Flask(__name__)


@dispatcher.add_method
def get_text(author):
    return sample.main(author)

@app.route("/rpc", methods=["POST"])
def index():
    req = request.get_data().decode()
    response = JSONRPCResponseManager.handle(req, dispatcher) 
    return Response(response.json, mimetype="application/json")


@app.route('/healthz')
def healthz():
    app.logger.info('Health checked')
    return jsonify({"status": "ok", "message": "Application {{cookiecutter.application_name}}"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)

