from flask import Flask, render_template,request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.app_context().push() #Isso geralmente significa que você tentou usar a funcionalidade que precisava do aplicativo atual. Para resolver isso, configure um contexto de aplicativo com
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clientes.sqlite3"  ##aqui vai o nome do banco de dados

db = SQLAlchemy(app) # passa todos dados do app para o banco, todas instruções

class clientes(db.Model): # criando relacionamento entre banco de dados e sistema
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
    return render_template('index.html')   
    
@app.route('/clientes', methods = ['GET','POST'])
def rotaCliente():
    
    return render_template('clientes.html',clientes=clientes.query.all())

@app.route('/novo_cliente' , methods=['GET','POST'])
def novoCliente(): 
    nome = request.form.get('nome') # vai pegar o nome do form html (capturar valores)
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    endereco = request.form.get('endereco')
    # verificar se o método chamado é o post
    
    cliente = clientes(nome,telefone,email,endereco) # valores que vem do formulario 
    db.session.add(cliente) # adiciona no db 
    db.session.commit()  # realiza mudanças
    #return redirect(url_for('rotaCliente')) # redireciona para a pagina lista cursos
    return render_template('addCliente.html')  

@app.route('/<int:id>/atualiza_cliente',methods= ['GET','POST'])
def atualiza_cliente(id):
    cliente = clientes.query.filter_by(id=id).first() # faz o filtro do curso pelo id
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        endereco = request.form['endereco']
        clientes.query.filter_by(id=id).update({'nome':nome , 'telefone': telefone , 'email': email, 'endereco': endereco }) #update ira alterar a lista
        db.session.commit()
        return redirect(url_for('rotaCliente'))
    return render_template('atualiza_cliente.html',cliente=cliente) # será retornado o curso

@app.route('/adicionar_despesa',methods= ['GET','POST'])
def adicionar_despesas():
    return render_template('despesas.html')


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