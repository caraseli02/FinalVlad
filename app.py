#Inicializar libreria/dependencias
from flask import Flask
from flask import render_template
from flask import request
import datetime
import random
#Paquete para Base de datos
from pymongo import MongoClient


app = Flask(__name__)

#Mongo URL Atlas
MONGO_URL_ATLAS = 'mongodb+srv://admin:root@cluster0-odxe4.mongodb.net/test?retryWrites=true&w=majority'

client = MongoClient(MONGO_URL_ATLAS, ssl_cert_reqs=False)
db = client['Notas']
collection = db['Notas']


#rutas
@app.route('/', methods=['GET', 'POST'])
def index():
    global dateInfo
    d = datetime.date(random.randrange(1900, 2020), random.randrange(1, 13), random.randrange(1, 31))
    d = str(d)
    if request.method == 'POST':
        title = request.form.get('title')
        nota = request.form.get('nota')
        # collection.delete_many({})
        collection.insert_one({'title': title, 'nota': nota, 'date': d})
        return render_template('index.html')
    return render_template('index.html',)

@app.route('/verNotas', methods=['GET', 'POST'])
def ver():
    datos = collection.find({},{'_id': 0})
    lista = list(datos)
    leng = len(lista)
    nota = list()
    title = list()
    date = list()
    for i in range(0, leng):
        nota.append(lista[i]['nota'])
        title.append(lista[i]['title'])
        date.append(lista[i]['date'])
    return render_template('verNotas.html', nota=nota, title=title, date=date, list=list, leng=leng)

    return render_template('verNotas.html')

if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
