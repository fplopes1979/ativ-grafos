from flask_sqlalchemy import SQLAlchemy
 
db =SQLAlchemy()
 
class GraphModel(db.Model):
    __tablename__ = "table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vertices = db.Column(db.String())
    arestas = db.Column(db.String())
    direcionado = db.Column(db.Integer())
    valorado = db.Column(db.Integer())
 
    def __init__(self, vertices,arestas,direcionado,valorado, id = None):
        if id:
            self.id = id
        self.vertices = vertices
        self.arestas= arestas
        self.direcionado = direcionado
        self.valorado = valorado
 
    def __repr__(self):
        return f"{self.vertices}:{self.id}"