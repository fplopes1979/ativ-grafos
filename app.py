import networkx as nx
from io import BytesIO
from os import abort
from flask import Flask, render_template, send_file, request, redirect
from models import db, GraphModel
from graph_functions import create_graph, create_graph_direct, ordem_tamanho, adjacentes_grau, par_vertices
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

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
        global vertices, arestas, direcionado, valorado
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


@app.route('/graph')
def graph():
    global G
    G = create_graph(vertices, arestas, direcionado, valorado)
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, with_labels=True, node_size=150, node_color="skyblue", node_shape="o", alpha=0.5, linewidths=4, font_size=14,
                     font_weight="bold", width=2, edge_color="grey")
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    plt.clf()

    return send_file(img, mimetype='image/png')


@app.route('/data/<int:id>', methods=['GET', 'POST'])
def RetrieveGraph(id):
    if request.method == 'POST':
        global v1, v2
        v1 = request.form['v1']
        v2 = request.form['v2']
        return redirect(f'/data/{id}/vert')

    if request.method == 'GET':
        G = create_graph(vertices, arestas, direcionado, valorado)
        graph = GraphModel.query.filter_by(id=id).first()

        if graph:
            ordem = ordem_tamanho(G)
            return render_template('data.html', graph=graph, ordem=ordem)
        return f"Graph with id ={id} Does not exist"


@app.route('/data/<int:id>/vert')
def vertice(id):
    graph = GraphModel.query.filter_by(id=id).first()
    if graph:
        G = create_graph(vertices, arestas, direcionado, valorado)
        no_direct = create_graph_direct(vertices, arestas, valorado)
        adjac = adjacentes_grau(G, v1, no_direct, direcionado)
        par = par_vertices(G, v1, v2)
        return render_template('vertices.html', graph=graph, adjacente=adjac, vert=v1, v2=v2, par_vertices=par)


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
