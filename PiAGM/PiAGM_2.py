import igraph as ig
import matplotlib.pyplot as plt
import networkx as nx

def igraph_to_networkx(ig_graph):
    """Промежуточный метод перевода графа в другой вид для визуализации"""
    nx_graph = nx.Graph()
    nx_graph.add_nodes_from(range(len(ig_graph.vs)))
    edges = [(edge.source, edge.target) for edge in ig_graph.es]
    nx_graph.add_edges_from(edges)
    return nx_graph

def draw_graphs():
    """Метод для визуализации графов"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    nx_er = igraph_to_networkx(er_graph)
    nx.draw(nx_er, ax=axes[0], node_size=50, node_color='lightblue',
            with_labels=False, edge_color='gray')
    axes[0].set_title('Модель Эрдёша-Реньи (ER)')

    nx_ba = igraph_to_networkx(ba_graph)
    nx.draw(nx_ba, ax=axes[1], node_size=50, node_color='lightgreen',
            with_labels=False, edge_color='gray')
    axes[1].set_title('Модель Барабаши-Альберт (BA)')

    nx_ws = igraph_to_networkx(ws_graph)
    nx.draw(nx_ws, ax=axes[2], node_size=50, node_color='lightcoral',
            with_labels=False, edge_color='gray')
    axes[2].set_title('Модель Ваттса-Строгаца (WS)')

    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    n = 50
    p = 0.15
    m = 4
    k = 8

    er_graph = ig.Graph.Erdos_Renyi(n=n, p=p)
    ba_graph = ig.Graph.Barabasi(n=n, m=m)
    ws_graph = ig.Graph.Watts_Strogatz(dim=1, size=n, nei=k // 2, p=p)

    draw_graphs()




    degrees = er_graph.degree()
    print(degrees)

    avg_clustering = er_graph.transitivity_avglocal_undirected()
    print(avg_clustering)

