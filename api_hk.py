from flask import Flask, jsonify, request
import requests

url = 'https://demoemisionv2.thefactoryhka.com.ve/api/EstadoDocumento'

datos = ""
app = Flask(__name__)

@app.route("/ping")
def root():
    return "Home"


@app.route('/products')
def getProduct():
    return jsonify({"Datos": datos})

@app.route('/products/<string:data_name>')
def getDato(data_name):
    [data for data in datos if data["name"] == data_name]
    return 'received'

if __name__ == '__main__':
    app.run(debug=True, port=4000)

