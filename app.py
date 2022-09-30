from os import abort
from flask import Flask, render_template, request, redirect
from models import db, GraphModel
from sqlalchemy import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def create():
    list = []
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        vertices = request.form['vertices']
        arestas = request.form['arestas']
        direcionado = request.form['direcionado']
        valorado = request.form['valorado']
        graph = GraphModel(
           vertices=vertices, arestas=arestas, direcionado=direcionado, valorado=valorado)
        db.session.add(graph)
        db.session.commit()

        for value in db.session.query(GraphModel.id):
            take_id = value[0]
            list.append(take_id)
        return redirect(f'/data/{list[-1]}')


@app.route('/data')
def RetrieveList():
    graphs = GraphModel.query.all()
    return render_template('datalist.html', graphs=graphs)


@app.route('/data/<int:id>')
def RetrieveGraph(id):
    graph = GraphModel.query.filter_by(id=id).first()
    if graph:
        return render_template('data.html', graph=graph)
    return f"Graph with id ={id} Does not exist"


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