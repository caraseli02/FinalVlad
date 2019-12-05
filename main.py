#Inicializar libreria/dependencias
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

#rutas 
@app.route('/', methods=['GET', 'POST'])
def inicio():
    return render_template('index.html')

if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)