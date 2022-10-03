import networkx as nx


def create_graph(vertices, arestas, direcionado, valorado):

    vertices = eval(vertices)
    arestas = eval(arestas)

    if direcionado == "1":
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    G.add_nodes_from(vertices)

    if valorado == "1":
        G.add_weighted_edges_from(arestas)
    else:
        G.add_edges_from(arestas)

    return (G)


def create_graph_direct(vertices, arestas, valorado):

    vertices = eval(vertices)
    arestas = eval(arestas)

    no_direct = nx.Graph()

    no_direct.add_nodes_from(vertices)

    if valorado == "1":
        no_direct.add_weighted_edges_from(arestas)
    else:
        no_direct.add_edges_from(arestas)

    return (no_direct)


def ordem_tamanho(graph):
    ordem = graph.number_of_nodes()
    tamanho = graph.number_of_edges()
    return ("Ordem: ", ordem, "Tamanho:", tamanho)


def adjacentes_grau(graph, node, no_direct, direcionado):
    node = eval(node)
    list = [n for n in graph.neighbors(node)]
    list_no_direct = [n for n in no_direct.neighbors(node)]

    if direcionado == "1":
        grau_saida = len(list)
        grau_entrada = len(list_no_direct) - len(list)
        setA = set(list_no_direct)
        setB = set(list)
        entrada = setA - setB
        text = """ Lista de vértices adjacentes: {}  |
        Grau de saída: {}  |
        Grau de entrada: {}  |
        Arestas que entram no vértice quando o grafo é direcionado: {}""".format(list, grau_saida, grau_entrada, entrada)
    else:
        grau = len(list)
        text = """ Lista de vértices adjacentes: {}  |
        Grau: {}""".format(list, grau)

    return text

def par_vertices(graph,v1,v2):
    v1 = eval(v1)
    v2 = eval(v2)
    tem_path = False
    tem_path = nx.has_path(graph, v1, v2)
    path, custo = [],0

    is_adjacent = False
    for n in graph.neighbors(v1):
        if n == v2:
            is_adjacent = True

    if(tem_path):
        path = nx.dijkstra_path(graph, source=v1, target=v2, weight='weight')
        custo = nx.dijkstra_path_length(graph, source=v1, target=v2)
    
    text = """ Adjacentes: {}  |
        Caminho mais curto: {}  |
        Custo: {}""".format(is_adjacent, path, custo)
    return (text)
