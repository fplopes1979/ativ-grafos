import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx


def create_graph(vertices, arestas, direcionado, valorado):

    if direcionado == "1":
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    G.add_nodes_from(vertices)

    if valorado == "1":
        G.add_weighted_edges_from(arestas)
    else:
        G.add_edges_from(arestas)

    ordem = G.number_of_nodes()

    tamanho = G.number_of_nodes() + G.number_of_edges()

    # pos = nx.spring_layout(G)
    # nx.draw_networkx(G, pos, with_labels=True)
    # labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # with open('graph.png', 'wb') as img:
    #     plt.savefig(img)
    #     plt.clf()

    return ("ordem: ",ordem,"\ntamanho: ",tamanho)  # to-do retornar o grafo
