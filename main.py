import pandas as pd

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for _ in range(vertices)] for _ in range(vertices)]
        self.edges = 0
        for i in range(vertices):
            self.graph[i][i] = 0

    def add_edge(self, u, v, w):
        self.edges += 1
        self.graph[u-1][v-1] = w
        self.graph[v-1][u-1] = w

    def display(self):
        vertices = [f'v{i}' for i in range(1, self.V+1)]
        df = pd.DataFrame(self.graph, index=vertices, columns=vertices)

        print("\nМатрица смежности:")
        print(df)

    """Матрица инцидентности"""
    def toIncidence_matrix(self):
        edge = 0
        incidence_matrix = [[0 for _ in range(self.edges)] for _ in range(self.V)]
        for row in range(len(self.graph)):
            for col in range(row, len(self.graph[row])):
                    if self.graph[row][col] != 0:
                        incidence_matrix[row][edge] = self.graph[row][col]
                        incidence_matrix[col][edge] = self.graph[row][col]
                        edge+=1

        vertices = [f'v{i}' for i in range(1, self.V+1)]
        edge = ['e1' for _ in range(1, self.edges+1)]
        df = pd.DataFrame(incidence_matrix, index=vertices, columns=edge)

        print("\nМатрица инцидентности:")
        print(df)

    """Матрица степеней"""
    def toDegrees_matrix(self):
        degrees_matrix = [[0 for _ in range(self.V)] for _ in range(self.V)]
        for row in range(self.V):
            degrees_matrix[row][row] = sum(self.graph[row])

        vertices = [f'v{i}' for i in range(1, self.V + 1)]
        df = pd.DataFrame(degrees_matrix, index=vertices, columns=vertices)

        print("\nМатрица степеней:")
        print(df)

    """Матрица достижимости"""
    def toReachability_matrix(self):
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


if __name__ == "__main__":
    g = Graph(7)
    g.add_edge(1, 2, 3)
    g.add_edge(1, 3, 5)
    g.add_edge(2, 3, 4)
    g.add_edge(4, 6, 1)
    g.add_edge(4, 5, 2)
    g.add_edge(5, 6, 3)

    g.display()

    g.toIncidence_matrix()

    g.toDegrees_matrix()

    g.toReachability_matrix()

    g.floyd_warshall()
