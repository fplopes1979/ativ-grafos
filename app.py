from os import abort
from flask import Flask, render_template, request, redirect
from models import db, GraphModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        id = request.form['id']
        vertices = request.form['vertices']
        arestas = request.form['arestas']
        direcionado = request.form['direcionado']
        valorado = request.form['valorado']
        graph = GraphModel(
            id=id, vertices=vertices, arestas=arestas, direcionado=direcionado, valorado=valorado)
        db.session.add(graph)
        db.session.commit()
        return redirect('/data/1')


@app.route('/data')
def RetrieveList():
    graphs = GraphModel.query.all()
    return render_template('datalist.html', graphs=graphs)


@app.route('/data/<int:id>')
def RetrieveGraph(id):
    graph = GraphModel.query.filter_by(id=id).first()
    if graph:
        return render_template('data.html', graph=graph)
    return f"Graph with id ={id} Doenst exist"


@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    graph = GraphModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if graph:
            db.session.delete(graph)
            db.session.commit()
            return redirect('/data')
        abort(404)

    return render_template('delete.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
