#Inicializar libreria/dependencias
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import datetime
import random
#Paquete para Base de datos
from pymongo import MongoClient


app = Flask(__name__)

#Mongo URL Atlas
MONGO_URL_ATLAS = 'mongodb+srv://admin:root@cluster0-odxe4.mongodb.net/test?retryWrites=true&w=majority'

client = MongoClient(MONGO_URL_ATLAS, ssl_cert_reqs=False)
db = client['Notas']
collection = db['NotasMovil']

class CREAR_NOTA:
    def __init__(self, name, note):
        self.name = name
        self.note = note


#rutas
@app.route('/', methods=['GET', 'POST'])
def index():
    global dateInfo
    dateInfo = datetime.datetime.now()
    d = dateInfo.strftime('%x')
    d = str(d)
    if request.method == 'POST':
        nota = request.form.get('nota')
        if nota == '':
            return render_template('index.html')
        else:
            collection.insert_one({ 'nota': nota, 'date': d, 'Title': 'Movil' })
            return render_template('index.html')
    return render_template('index.html',)

@app.route('/verNotas', methods=['GET', 'POST'])
def ver():
    datos = collection.find({})
    lista = list(datos)
    leng = len(lista)
    nota = list()
    title = list()
    date = list()
    for i in range(0, leng):
        title.append(lista[i]['Title'])
        nota.append(lista[i]['nota'])
        date.append(lista[i]['date'])
    return render_template('verNotas.html', nota=nota, date=date, lista=lista, leng=leng,title=title)

    return render_template('verNotas.html')

@app.route('/delete/<path:nota>')
def delete(nota):
    collection.delete_one({'nota': nota})
    return redirect('/verNotas')

@app.route('/actualiarNotas/<path:actulize>', methods = ['GET' , 'POST'])
def actualiarNotas(actulize):
    note = collection.find({'title': actulize})

    if request.method == 'POST':
        # note.content = request.form['content']
        title = request.form.get('title')
        nota = request.form.get('nota')

        collection.update_one({'title': actulize}, {
                '$set' : {'title': title, 'nota':nota}
            })
        return redirect('/verNotas')


    else:
        return render_template('actualiarNotas.html', note = list(note))

@app.route('/verTitles')
def verTitles():
    
    return render_template('verTitles.html')




if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
