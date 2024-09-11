# verifico a pasta do meu projeto, verifico se está no meu github
# git remote -v
# executar
# git pull origin master(main)

# quero clonar meu projeto em uma pasta vazia
# git clone https://caminho_do_projeto .
# instalo a extensão do python
# abro o terminal e verifico se abre no venv, caso não abra eu devo executar
# ctrl shift p
# e digitar envioronment e pedir para criar um ambiente virtual 

# pip install flask
# pip install Flask-SQLAlchemy
# pip install Flask-Migrate
# pip install Flask-Script
# pip install pymysql
# flask db init
# executo quando não tenho a pasta migrations
# flask db migrate -m "Migração Inicial"
# executo qunado não tenho python na pasta versions
# flask db upgrade
# executo quando minhas tabelas não estão criadas no meu banco de dados

from flask import Flask, render_template, request, flash, redirect
from database import db
from flask_migrate import Migrate
from models import Agendamento

app = Flask(__name__)
app.config['SECRET_KEY'] = 'JHEXDY'
# drive://usuario:senha@servidor/banco_dados
conexao = "mysql+pymysql://alunos:cefetmg@127.0.0.1/flaskg1"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aula')
@app.route('/aula/<nome>')
@app.route('/aula/<nome>/<curso>/<int:ano>')
def aula(nome = 'Maria', curso = 'Informáica', ano = 1):
    dados = {'nome': nome, 'curso': curso, 'ano': ano}
    return render_template('aula.html', dados_html=dados)

@app.route('/agendamento')
def agendamento():
    u = Agendamento.query.all()
    return render_template('agendamento_lista.html', dados = u)

@app.route('/agendamento/add')
def agendamento_add():
    return render_template('agendamento_add.html')

@app.route('/agendamento/save', methods=['POST'])
def agendamento_save():
    id = request.form.get('id')
    data = request.form.get('data')
    cliente = request.form.get('cliente')
    servico = request.form.get('servico')
    if data and cliente and servico:
        agendamento = Agendamento(data, cliente, servico)
        db.session.add(agendamento)
        db.session.commit()
        flash('Agendamento cadastrado com sucesso!!!')
        return redirect('/agendamento')
    else:
        flash('Preencha todos os campos!!!')
        return redirect('/agendamento/add')

@app.route('/agendamento/remove/<int:id>')
def agendamento_remove(id):
    if id > 0:
        agendamento = Agendamento.query.get(id)
        db.session.delete(agendamento)
        db.session.commit()
        flash('Agendamento removido com sucesso!!!')
        return redirect('/agendamento')
    else:
        flash('Caminho incorreto!!!')
        return redirect('/agendamento')
    
@app.route('/agendamento/edita/<int:id>')
def agendamento_edita(id):
    agendamento = Agendamento.query.get(id)
    return render_template('agendamento_edita.html', dados = agendamento)

@app.route('/agendamento/editsave', methods=['POST'])
def agendamento_editasave():
    id = request.form.get('id')
    data = request.form.get('data')
    cliente = request.form.get('cliente')
    servico = request.form.get('servico')
    if id and data and cliente and servico:
        agendamento = Agendamento.query.get(id)
        agendamento.id = id
        agendamento.data = data
        agendamento.cliente = cliente
        agendamento.servico = servico
        db.session.commit()
        flash('Dados atualizados com sucesso!!!')
        return redirect('/agendamento')
    else:
        flash('Faltando dados!!!')
        return redirect('/agendamento')
       
if __name__ == '__main__':
    app.run()