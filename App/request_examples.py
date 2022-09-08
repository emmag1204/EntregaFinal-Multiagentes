import requests

URL = 'http://127.0.0.1:5000'

json_example = {
    'agente':1,
    'posicion': {
        'x':10,
        'y':20
    }
}

r = requests.post(url = URL+"/agentpy_json", json=json_example)

print(r.text)