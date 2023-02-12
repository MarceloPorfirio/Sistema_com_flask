from flask import Flask, render_template,request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.app_context().push() #Isso geralmente significa que você tentou usar a funcionalidade que precisava do aplicativo atual. Para resolver isso, configure um contexto de aplicativo com
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cursos.sqlite3"  ##aqui vai o nome do banco de dados

db = SQLAlchemy(app) # passa todos dados do app para o banco, todas instruções

frutas = [] #declarando fora do escopo, ela fica globalmente e vai adicionando os itens
registros = [] # colocar os dicionarios dentro de uma lista

class cursos(db.Model): # criando relacionamento entre banco de dados e sistema
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    telefone = db.Column(db.String(50))
    email = db.Column(db.String(50))
    endereco = db.Column(db.String(50))

    def __init__(self,nome,telefone,email,endereco): # metodo de construção
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.endereco = endereco

@app.route('/',methods = ['GET','POST'])     
def primeiraRota():
    #frutas = ['Maça', 'Banana', 'Uva', 'Laranja']
    #frutas =[] declarando a lista dentro da função, sempre será substituida
    if request.method =='POST': #verifica se é o metodo poat utilizado
        if request.form.get('fruta'): # verifica se algo foi escrito
            frutas.append(request.form.get('fruta')) # adiciona o item digitado na lista

    return render_template('index.html',frutas = frutas)   
    


if __name__ == '__main__':
    db.create_all() 

    ''' Isso ocorre porque você nunca fornece a SESSION_TYPEconfiguração para Flask ;
     não basta configurá-lo como global em seu módulo. 
     O código de exemplo de início rápido Flask-Session define um global, 
     mas usa o módulo atual como um objeto de configuração chamando app.config.from_object(__name__).
     Erro corrigido com o cod abaixo'''

    app.secret_key = 'super secret key'     
    app.config['SESSION_TYPE'] = 'filesystem'
        
    app.run(debug=True) 