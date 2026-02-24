import pandas as pd

class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.V = len(graph)
        self.edges = 0

        for row in range(len(self.graph)):
            for col in range(row, len(self.graph[row])):
                    if self.graph[row][col] != 0:
                        self.edges+=1


    def add_edge(self, u, v, w):
        self.edges += 1
        self.graph[u-1][v-1] = w
        self.graph[v-1][u-1] = w

    def add_vertices(self):
        new_graph = self.graph
        for row in range(self.V):
            new_graph[row].append(0)

        self.V += 1
        new_graph.append([0 for _ in range(self.V)])
        self.graph = new_graph

    def add_node(self, u, v, w):
        self.edges += 1
        self.graph[u - 1][v - 1] = w
        self.graph[v - 1][u - 1] = w

    """матрица смежности"""
    def to_adjacency_matrix(self):
        vertices = [f'' for i in range(1, self.V+1)]
        df = pd.DataFrame(self.graph, index=vertices, columns=vertices)

        print("\nМатрица смежности:")
        print(df)

    """Матрица инцидентности"""
    def to_incidence_matrix(self):
        edge = 0
        incidence_matrix = [[0 for _ in range(self.edges)] for _ in range(self.V)]
        for row in range(len(self.graph)):
            for col in range(row, len(self.graph[row])):
                    if self.graph[row][col] != 0:
                        incidence_matrix[row][edge] = self.graph[row][col]
                        incidence_matrix[col][edge] = self.graph[row][col]
                        edge+=1

        vertices = [f'v{i}' for i in range(1, self.V+1)]
        edge = [f'e{i}' for i in range(1, self.edges+1)]
        df = pd.DataFrame(incidence_matrix, index=vertices, columns=edge)

        print("\nМатрица инцидентности:")
        print(df)

    """Матрица степеней"""
    def to_degrees_matrix(self):
        degrees_matrix = [[0 for _ in range(self.V)] for _ in range(self.V)]
        for row in range(self.V):
            degrees_matrix[row][row] = sum(self.graph[row])

        vertices = [f'v{i}' for i in range(1, self.V + 1)]
        df = pd.DataFrame(degrees_matrix, index=vertices, columns=vertices)

        print("\nМатрица степеней:")
        print(df)

    """Матрица достижимости"""
    def to_reachability_matrix(self):
        reachability_matrix = [[0 for _ in range(self.V)] for _ in range(self.V)]
        for row in range(len(self.graph)):
            for col in range(row, len(self.graph[row])):
                if self.graph[row][col] != 0:
                    reachability_matrix[row][col] = 1
                    reachability_matrix[col][row] = 1
            reachability_matrix[row][row] = 1

        vertices = [f'v{i}' for i in range(1, self.V + 1)]
        df = pd.DataFrame(reachability_matrix, index=vertices, columns=vertices)

        print("\nМатрица достижимости:")
        print(df)

    """Матрица расстояний"""
    def floyd_warshall(self):
        dist = self.graph

        for k in range(self.V):
            for i in range(self.V):
                for j in range(self.V):
                    if dist[i][k] != 0 and dist[k][j] != 0:
                        if dist[i][j] > dist[i][k] + dist[k][j]:
                            dist[i][j] = dist[i][k] + dist[k][j]

        vertices = [f'v{i}' for i in range(1, self.V + 1)]
        df = pd.DataFrame(dist, index=vertices, columns=vertices)

        print("\nМатрица расстояний:")
        print(df)

    """Матрица Кирхгофа"""
    def to_kirchhoff_matrix(self):
        kirchhoff_matrix = [[0 for _ in range(self.V)] for _ in range(self.V)]
        for row in range(self.V):
            for col in range(self.V):
                kirchhoff_matrix[row][col] = self.graph[row][col] * (-1)
            kirchhoff_matrix[row][row] = sum(self.graph[row])

        vertices = [f'v{i}' for i in range(1, self.V + 1)]
        df = pd.DataFrame(kirchhoff_matrix, index=vertices, columns=vertices)

        print("\nМатрица Кирхгофа:")
        print(df)

    def to_ring_sum_matrix(self, add_graph):
        size = max(self.V, len(add_graph))
        ring_sum_matrix = [[0] * size for _ in range(size)]

        for i in range(self.V):
            for j in range(self.V):
                ring_sum_matrix[i][j] = self.graph[i][j]

        overlap = min(self.V, len(add_graph))
        for i in range(overlap):
            for j in range(overlap):
                ring_sum_matrix[i][j] ^= add_graph[i][j]

        vertices = [f'v{i + 1}' for i in range(size)]
        df = pd.DataFrame(ring_sum_matrix, index=vertices, columns=vertices)
        print("\nКольцевая сумма графов:")
        print(df)

if __name__ == "__main__":
    g1 = Graph([
        [0, 3, 5, 0, 0, 0, 0],
        [3, 0, 4, 0, 0, 0, 0],
        [5, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 1, 0],
        [0, 0, 0, 2, 0, 3, 0],
        [0, 0, 0, 1, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
               ])

    g1.to_adjacency_matrix()

    g1.to_incidence_matrix()

    g1.to_degrees_matrix()

    g1.to_reachability_matrix()

    g1.floyd_warshall()

    g1.to_kirchhoff_matrix()

    g2 = Graph([
        [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 1, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 0, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 0, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
    ])

    g2.add_vertices()

    g2.to_adjacency_matrix()

    g2.add_node(8, 1, 10)

    g2.to_adjacency_matrix()

    g3 = Graph([
        [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 1, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 0, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 0, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
    ])

    g3.to_ring_sum_matrix(add_graph=[
    [0, 1, 1, 0, 1, 0],
    [1, 0, 1, 1, 0, 1],
    [1, 1, 0, 1, 1, 0],
    [0, 1, 1, 0, 1, 1],
    [1, 0, 1, 1, 0, 1],
    [0, 1, 0, 1, 1, 0]
])


