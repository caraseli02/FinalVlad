# Inicializar libreria/dependencias
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
import datetime
import random
# Paquete para Base de datos
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Mongo URL Atlas
MONGO_URL_ATLAS = 'mongodb+srv://admin:root@cluster0-odxe4.mongodb.net/test?retryWrites=true&w=majority'

client = MongoClient(MONGO_URL_ATLAS, ssl_cert_reqs=False)
db = client['Notas']
collection = db['NotasMovil']


class CREAR_NOTA:
    def __init__(self, name, note):
        self.name = name
        self.note = note


# rutas
@app.route('/', methods=['GET', 'POST'])
def index():
    global dateInfo
    dateInfo = datetime.datetime.now()
    d = dateInfo.strftime('%x')
    d = str(d)
    if request.method == 'POST':
        nota = request.form.get('nota')
        title = request.form.get('title')
        if nota == '':
            return render_template('index.html')
        else:
            collection.insert_one({'nota': nota, 'date': d, 'title': title})
            flash(f'Note created: {d}')
            return render_template('index.html')
    return render_template('index.html', )


@app.route('/verNotas', methods=['GET', 'POST'])
def ver():
    if request.method == 'POST':
        src = request.form.get('search')
        datos = collection.find({
            "nota": {"$regex": src, '$options': 'si'},
            "title": {"$regex": src, '$options': 'si'}
        })
        lista = list(datos)
        leng = len(lista)
        nota = list()
        title = list()
        title_links = set()
        date = list()
        try:
            for i in range(0, leng):
                title.append(lista[i]['title'])
                title_links.add(lista[i]['title'])
                nota.append(lista[i]['nota'])
                date.append(lista[i]['date'])
            return render_template('verNotas.html', nota=nota,
                                   date=date, lista=lista, leng=leng, title=title, title_links=title_links)
        except ValueError:
            return 'ErrorResponse'
    datos = collection.find({})
    lista = list(datos)
    leng = len(lista)
    nota = list()
    title = list()
    title_links = set()
    date = list()
    try:
        for i in range(0, leng):
            title.append(lista[i]['title'])
            title_links.add(lista[i]['title'])
            nota.append(lista[i]['nota'])
            date.append(lista[i]['date'])
        return render_template('verNotas.html', nota=nota,
                               date=date, lista=lista, leng=leng, title=title, title_links=title_links)
    except ValueError:
        return 'ErrorResponse'
    return render_template('verNotas.html')


@app.route('/delete/<path:nota>')
def delete(nota):
    collection.delete_one({'nota': nota})
    return redirect('/verNotas')


@app.route('/actualiarNotas/<path:actulize>', methods=['GET', 'POST'])
def actualiarNotas(actulize):
    note = collection.find({'nota': actulize})
    dateInfo = datetime.datetime.now()
    d = dateInfo.strftime('%x')
    d = str(d)

    if request.method == 'POST':
        # note.content = request.form['content']
        title = request.form.get('title')
        nota = request.form.get('nota')
        if nota == "" or title == "":
            flash('Tienes que completar todo')
            return redirect(request.url)
        collection.update_one({'nota': actulize}, {
            '$set': {'title': title, 'nota': nota}
        })
        flash(f'Note updated: {d}')
        return redirect('/verNotas')

    else:
        return render_template('actualiarNotas.html', note=list(note))


@app.route('/verNotas/<path:title_link>', methods=['GET', 'POST'])
def selectTitle(title_link):
    Tlink = collection.find({
        "title": {"$regex": title_link, '$options': 'si'}
    })
    titlesDB = list(collection.find({}, {"title": 1, "_id": 0}))
    lista = list(Tlink)
    leng = len(lista)
    nota = list()
    title = list()
    title_links = set()
    for t in titlesDB:
        title_links.add(t["title"])
    date = list()
    try:
        for i in range(0, leng):
            title.append(lista[i]['title'])
            # title_links.add(titlesDB[i]['title'])
            nota.append(lista[i]['nota'])
            date.append(lista[i]['date'])
        return render_template('verNotas.html', nota=nota,
                               date=date, lista=lista, leng=leng, title=title, title_links=title_links,
                               titlesDB=titlesDB, title_link=title_link)
    except ValueError:
        return 'ErrorResponse'


if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
