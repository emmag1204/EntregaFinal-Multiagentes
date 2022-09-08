from crypt import methods
from flask import Flask, request
from flask_json import FlaskJSON

app = Flask(__name__)
json = FlaskJSON(app)

@app.route("/agentpy_json", methods = ['POST'])
def agentpy_send_data():
    data = request.get_json(force=True)
    print(data)
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run()

