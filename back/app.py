from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/jogos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Jogo(db.Model):
    __tablename__ = 'jogos' #nome da tabela
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(20), nullable=False)
    genero = db.Column(db.String(20), nullable=False)
    classificacao = db.Column(db.String(10), nullable=False)
    plataforma = db.Column(db.String(10), nullable=False)
    

    def to_json(self): #converte cada registro num JSON em formato de dicionário
        json_jogos = {
            'id': self.id,
            'titulo': self.titulo,
            'genero': self.genero,
            'classificacao': self.classificacao,
            'plataforma': self.plataforma
        }
        return json_jogos

    @staticmethod
    def from_json(json_jogos): #recebe os dados a serem incluidos
        titulo = json_jogos.get('titulo')
        genero = json_jogos.get('genero')
        classificacao = json_jogos.get('classificacao')
        plataforma = json_jogos.get('plataforma')
        # retorna objeto Jogo
        return Jogo(titulo=titulo, genero=genero, classificacao=classificacao, plataforma=plataforma)


@app.route('/jogos')
@cross_origin()
def cadastro():
    # obtém todos os registros da tabela filmes em ordem de titulo
    jogos = Jogo.query.order_by(Jogo.titulo).all()
    # converte a lista de jogos para o formato JSON
    # list comprehensions
    return jsonify([jogo.to_json() for jogo in jogos])


@app.route('/jogos', methods=['POST'])
@cross_origin()
def inclusao():
    #converte os dados que vierem em formato JSON no objeto jogo
    jogo = Jogo.from_json(request.json)

    # se campo tiver algum conteúdo
    # if !filme.titulo or !filme.genero or !filme.duracao or !filme.nota

    # if '' or 0 in filme.to_json().values()

    # list comprehensions
    erros = [campo for campo, valor in jogo.to_json().items()
             if valor == '']

    # em Python, JS... 0 => False; qualquer valor (exceto 0) => True
    if len(erros):
        return jsonify({'id': 0, 'message': ','.join(erros) + ' deve(m) ser preenchido(s)'}), 400

    db.session.add(jogo) # adiciona o objeto filme na tabela
    db.session.commit() # persiste os dados
    return jsonify(jogo.to_json()), 201


@app.route('/jogos/<int:id>')
@cross_origin()
def consulta(id):
    # obtém o registro a ser alterado (ou gera um erro 404 - not found)
    jogo = Jogo.query.get_or_404(id)
    return jsonify(jogo.to_json()), 200


@app.errorhandler(404)
@cross_origin()
def id_invalido(error):
    return jsonify({'id': 0, 'message': 'not found'}), 404


@app.route('/jogos/<int:id>', methods=['PUT'])
@cross_origin()
def alteracao(id):
    # obtém o registro a ser alterado (ou gera um erro 404 - not found)
    jogo = Jogo.query.get_or_404(id)

    # recupera os dados enviados na requisição
    jogo.titulo = request.json['titulo']
    jogo.genero = request.json['genero']
    jogo.classificacao = request.json['classificacao']
    jogo.plataforma = request.json['plataforma']

    # altera (pois o id já existe)
    db.session.add(jogo)
    db.session.commit()
    return jsonify(jogo.to_json()), 204


@app.route('/jogos/<int:id>', methods=['DELETE'])
@cross_origin()
def exclui(id):
    Jogo.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'id': id, 'message': 'Jogo excluído com sucesso'}), 200


@app.route('/jogos/pesq/<palavra>')
@cross_origin()
def pesquisa(palavra):
    # obtém todos os registros da tabela filmes em ordem de titulo
    jogos = Jogo.query.order_by(Jogo.titulo).filter(
        Jogo.titulo.like(f'%{palavra}%')).all()
    # converte a lista de filmes para o formato JSON (list comprehensions)
    return jsonify([jogo.to_json() for jogo in jogos])


@app.route('/')
def teste():
    return '<h1>Cadastro de Jogos</h1>'


if __name__ == '__main__':
    app.run(debug=True)
