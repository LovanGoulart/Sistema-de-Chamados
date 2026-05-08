from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import case, or_

app = Flask(__name__)
app.secret_key = 'supersecret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helpdesk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#------------------------------------------------------MODELOS----------------------------------------------------------------------------
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(200))
    tipo = db.Column(db.String(50))   

class Chamado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    solicitante = db.Column(db.String(100))
    local = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    status = db.Column(db.String(50), default='Aberto')
    prioridade = db.Column(db.String(50))
    data_abertura = db.Column(db.DateTime, default=datetime.now)
    descricao_solucao = db.Column(db.Text)
    tecnico = db.Column(db.String(100))
    data_resolucao = db.Column(db.DateTime, nullable=True)  # ✅ CORRIGIDO
    data_manutencao = db.Column(db.DateTime)
    destino = db.Column(db.String(50))  # quem vai atender

#---------------------------------------------------ROTAS---------------------------------------------------------------
@app.route('/')
def inicio():
    return render_template('inicio.html')

#-------------------------------------------------DASHBOARD-------------------------------------------------------------
from sqlalchemy import case, func

@app.route('/dashboard')
def dashboard():

    if 'tipo' not in session:
        return redirect('/login')

    if session['tipo'] == 'Usuario':
        return redirect('/meus')

    if session['tipo'] == 'Admin':
        chamados = Chamado.query
    else:
        chamados = Chamado.query.filter_by(destino=session['tipo'])

    chamados = chamados.filter(
        Chamado.status.in_(['Aberto', 'Em andamento'])
    ).order_by(

        # 🔥 PRIORIDADE MÁXIMA → DATA MANUTENÇÃO HOJE
        case(
            (
                func.date(Chamado.data_manutencao) == func.current_date(),
                0
            ),
            else_=1
        ),

        # 🔥 SUA REGRA ORIGINAL (mantida)
        case(
            (
                (Chamado.status == 'Em andamento') &
                (Chamado.tecnico == session['user']),
                1
            ),
            (Chamado.status == 'Aberto', 2),
            (Chamado.status == 'Em andamento', 3),
            else_=4
        ),

        case(
            (Chamado.prioridade == 'Alta', 1),
            (Chamado.prioridade == 'Média', 2),
            (Chamado.prioridade == 'Baixa', 3),
            else_=4
        ),

        Chamado.data_abertura.desc()

    ).all()

    return render_template('dashboard.html', chamados=chamados, now=datetime.now())
#--------------------------------------------------LOGIN-------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Usuario.query.filter_by(email=request.form['email']).first()

        if user and check_password_hash(user.senha, request.form['senha']):
            session['user'] = user.nome
            session['tipo'] = user.tipo

            # 🔥 REDIRECIONAMENTO INTELIGENTE
            if user.tipo == 'Usuario':
                return redirect('/meus')
            else:
                return redirect('/dashboard')

    return render_template('login.html')

#----------------------------------------------------LOGOUT-------------------------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

#---------------------------------------------CADASTRO DE USUÁRIO---------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        email = request.form['email']
        user_existente = Usuario.query.filter_by(email=email).first()

        # 🔥 SE JÁ EXISTE → MOSTRA ERRO
        if user_existente:
            return render_template(
                'register.html',
                erro="Email já cadastrado. Faça login."
            )

        # 🔥 CRIA USUÁRIO
        user = Usuario(
            nome=request.form['nome'],
            email=email,
            senha=generate_password_hash(request.form['senha']),
            tipo=request.form['tipo']
        )

        db.session.add(user)
        db.session.commit()

        # 🔥 REDIRECIONA PRO LOGIN COM MENSAGEM
        return redirect('/login?sucesso=1')

    return render_template('register.html')

#-----------------------------------------------------NOVO CHAMADO-------------------------------------------------------
from datetime import datetime

@app.route('/novo', methods=['GET', 'POST'])
def novo():
    if request.method == 'POST':

        # 🔥 pega a data (pode vir vazia)
        data_manutencao = request.form.get('data_manutencao')

        # 🔥 trata corretamente
        if data_manutencao:
            data_manutencao = datetime.strptime(request.form['data_manutencao'],'%Y-%m-%d %H:%M')
        else:
            data_manutencao = None

        chamado = Chamado(
            solicitante=request.form['solicitante'],
            local=request.form['local'],
            descricao=request.form['descricao'],
            prioridade=request.form['prioridade'],
            destino=request.form['destino'],
            status='Aberto',
            data_manutencao=data_manutencao  # 🔥 agora seguro
        )

        db.session.add(chamado)
        db.session.commit()

        return redirect('/dashboard')

    return render_template('novo.html')

#------------------------------------------------TODOS OS CHAMADOS------------------------------------------------------
@app.route('/todos')
def todos():
        # 🔒 usuário não logado

    if 'tipo' not in session:
        return redirect('/login')

    # 🔒 BLOQUEIA usuário comum
    if session['tipo'] == 'Usuario':
        return redirect('/meus')

    # 🔥 ADMIN vê tudo
    if session['tipo'] == 'Admin':
        chamados = Chamado.query

   # 🔥 OUTROS veem só os chamados do setor
    else:
        chamados = Chamado.query.filter_by(destino=session['tipo'])
        
        chamados = chamados.order_by(
        case(
            (
                (Chamado.status == 'Em andamento') &
                (Chamado.tecnico == session['user']),
                1
            ),
            (Chamado.status == 'Aberto', 2),
            (Chamado.status == 'Em andamento', 3),
            (Chamado.status == 'Resolvido', 4),
            else_=5
        ),
        case(
            (Chamado.prioridade == 'Alta', 1),
            (Chamado.prioridade == 'Média', 2),
            (Chamado.prioridade == 'Baixa', 3),
            else_=4
        ),
        case(
            (Chamado.status == 'Aberto', Chamado.data_abertura),
            else_=None
        ).desc(),
        case(
            (Chamado.status == 'Resolvido', Chamado.data_resolucao),
            else_=None
        ).desc()
    ).all()

    return render_template('todos.html', chamados=chamados)
#---------------------------------------------------------TÉCNICO--------------------------------------------------------------
@app.route('/tecnico')
def tecnico():
    chamados = Chamado.query.order_by(
        Chamado.data_abertura.desc()
    ).all()

    return render_template('tecnico.html', chamados=chamados)

#-----------------------------------------------------RESOLVER CHAMADO---------------------------------------------------------
@app.route('/resolver/<int:id>', methods=['GET', 'POST'])
def resolver(id):

        # 🔒 usuário não logado
        
    if 'tipo' not in session:
        return redirect('/login')

    # 🔒 BLOQUEIA usuário comum
    if session['tipo'] == 'Usuario':
        return redirect('/meus')

    # 🔥 ADMIN vê tudo
    if session['tipo'] == 'Admin':
        chamado = Chamado.query

    

    chamado = Chamado.query.get_or_404(id)

    if request.method == 'POST':
        chamado.status = 'Resolvido'
        chamado.descricao_solucao = request.form['solucao']
        chamado.tecnico = session.get('user')
        chamado.data_resolucao = datetime.now()  # ✅ corrigido

        db.session.commit()

        return redirect('/dashboard')

    return render_template('resolver.html', chamado=chamado)

#--------------------------------------------------------ANDAMENTO--------------------------------------------------------------
@app.route('/andamento/<int:id>')
def andamento(id):

    chamado = Chamado.query.get_or_404(id)

    # 🔥 BLOQUEIA se já estiver em andamento
    if chamado.status == 'Em andamento':
        return redirect('/dashboard')  # ou flash("Já está em andamento")

    # 🔥 ALTERA STATUS
    chamado.status = 'Em andamento'
    chamado.tecnico = session['user']

    db.session.commit()

    return redirect('/dashboard')

#----------------------------------------------------------MEUS-----------------------------------------------------------
@app.route('/meus')
def meus():
    if 'user' not in session: 
        return redirect('/login')

    chamados = Chamado.query.filter_by(
        solicitante=session.get('user')
    ).order_by(case(
            (Chamado.status == 'Aberto', 1),
            (Chamado.status == 'Em andamento', 2),
            else_=3
        ),
        case(
            (Chamado.prioridade == 'Alta', 1),
            (Chamado.prioridade == 'Média', 2),
            (Chamado.prioridade == 'Baixa', 3),
            else_=4
        ),
        case(
            (Chamado.status == 'Aberto', Chamado.data_abertura),   # 👈 Abertos: ordem crescente
            else_=None
        ).desc(),
        case(
            (Chamado.status == 'Resolvido', Chamado.data_resolucao),   # 👈 Resolvidos: ordem decrescente
            else_=None
        ).desc()).all()

    return render_template('meus.html', chamados=chamados)

#--------------------------------------------------------INIT----------------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=5000, debug=True)

