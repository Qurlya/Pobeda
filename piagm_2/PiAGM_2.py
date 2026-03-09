import os

import igraph as ig
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import pickle

def igraph_to_networkx(ig_graph):
    """Промежуточный метод перевода графа в другой вид для визуализации"""
    nx_graph = nx.Graph()
    nx_graph.add_nodes_from(range(len(ig_graph.vs)))
    edges = [(edge.source, edge.target) for edge in ig_graph.es]
    nx_graph.add_edges_from(edges)
    return nx_graph

def draw_graphs(er_graph, ba_graph, ws_graph, n):
    """Метод для визуализации графов"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    nx_er = igraph_to_networkx(er_graph)
    nx.draw(nx_er, ax=axes[0], node_size=n, node_color='lightblue',
            with_labels=False, edge_color='gray')
    axes[0].set_title('Модель Эрдёша-Реньи (ER)')

    nx_ba = igraph_to_networkx(ba_graph)
    nx.draw(nx_ba, ax=axes[1], node_size=n, node_color='lightgreen',
            with_labels=False, edge_color='gray')
    axes[1].set_title('Модель Барабаши-Альберт (BA)')

    nx_ws = igraph_to_networkx(ws_graph)
    nx.draw(nx_ws, ax=axes[2], node_size=n, node_color='lightcoral',
            with_labels=False, edge_color='gray')
    axes[2].set_title('Модель Ваттса-Строгаца (WS)')

    plt.tight_layout()
    plt.show()


def plot_degree_distribution(er_graph, ba_graph, ws_graph):
    """Построение гистограмм распределения степеней"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    degrees_er = er_graph.degree()
    axes[0].hist(degrees_er, bins=range(min(degrees_er), max(degrees_er) + 2, 1), color='lightblue', edgecolor='black', align='left')
    axes[0].set_title('Распределение степеней (ER)')
    axes[0].set_xlabel('Степень вершины')
    axes[0].set_ylabel('Частота')

    degrees_ba = ba_graph.degree()
    axes[1].hist(degrees_ba, bins=range(min(degrees_ba), max(degrees_ba) + 2, 1), color='lightgreen', edgecolor='black', align='left')
    axes[1].set_title('Распределение степеней (BA)')
    axes[1].set_xlabel('Степень вершины')
    axes[1].set_ylabel('Частота')

    degrees_ws = ws_graph.degree()
    axes[2].hist(degrees_ws, bins=range(min(degrees_ws), max(degrees_ws) + 2, 1), color='lightcoral', edgecolor='black', align='left')
    axes[2].set_title('Распределение степеней (WS)')
    axes[2].set_xlabel('Степень вершины')
    axes[2].set_ylabel('Частота')

    plt.tight_layout()
    plt.show()


def analyze_graph(graph):

    avg_clustering = graph.transitivity_avglocal_undirected()

    diameter = graph.diameter()

    avg_path_length = graph.average_path_length()

    density = graph.density()

    components = graph.components()
    num_components = len(components)
    giant_component_size = components.giant().vcount()

    result = {
        'Средний коэффициент кластеризации': avg_clustering,
        'Диаметр графа': diameter,
        'Средняя длина пути': avg_path_length,
        'Плотность графа': density,
        'Количество компонент связности': num_components,
        'Размер гигантской компоненты': giant_component_size
    }

    return result

def save_graphs(er_graph, ba_graph, ws_graph, filename="graphs.pkl"):
    """Сохранение графов в файл"""
    with open(filename, 'wb') as f:
        pickle.dump({'er': er_graph, 'ba': ba_graph, 'ws': ws_graph}, f)

def load_graphs(filename="graphs.pkl"):
    """Загрузка графов из файла"""
    with open(filename, 'rb') as f:
        graphs = pickle.load(f)
    return graphs['er'], graphs['ba'], graphs['ws']

if __name__ == "__main__":
    n = 50
    p_er = 0.15
    m = 4
    k = 8
    p_ws = 0.3

    filename_3 = "graphs_original.pkl"
    filename_original = "graphs_3.pkl"
    filename_5 = "graphs_5.pkl"

    if os.path.exists(filename_3):
        er_graph, ba_graph, ws_graph = load_graphs(filename_original)
    else:
        er_graph = ig.Graph.Erdos_Renyi(n=n, p=p_er)
        ba_graph = ig.Graph.Barabasi(n=n, m=m)
        ws_graph = ig.Graph.Watts_Strogatz(dim=1, size=n, nei=k // 2, p=p_ws)
        save_graphs(er_graph, ba_graph, ws_graph, filename_original)

    draw_graphs(er_graph, ba_graph, ws_graph, n)
    plot_degree_distribution(er_graph, ba_graph, ws_graph)

    er_results = analyze_graph(er_graph)
    ba_results = analyze_graph(ba_graph)
    ws_results = analyze_graph(ws_graph)

    comparison_df = pd.DataFrame({
        'Модель ER': er_results,
        'Модель BA': ba_results,
        'Модель WS': ws_results
    })

    print(comparison_df)


