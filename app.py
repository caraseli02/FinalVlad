#Inicializar libreria/dependencias
from flask import Flask
from flask import render_template
from flask import request
#Paquete para Base de datos
from pymongo import MongoClient

app = Flask(__name__)

#Mongo URL Atlas
MONGO_URL_ATLAS = 'mongodb+srv://admin:root@cluster0-ypkpe.azure.mongodb.net/test?retryWrites=true&w=majority'

client = MongoClient(MONGO_URL_ATLAS, ssl_cert_reqs=False)
db = client['Inserted']
collection = db['Worlds']

#rutas
@app.route('/', methods=['GET', 'POST'])
def inicio():
    return render_template('index.html')

if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
