import networkx as nx
import matplotlib.pyplot as plt
import sys
import time

# -----------------------------
# 1. Данные графа
# -----------------------------
vertices = ["Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun"]
n = len(vertices)

adjacency_matrix = [
    [0, 0, 0, 2, 0, 0, 0],  # Mon
    [3, 0, 6, 0, 0, 2, 0],  # Tue
    [0, 0, 0, 8, 0, 0, 0],  # Wed
    [0, 0, 0, 0, 0, 0, 0],  # Thr
    [0, 0, 7, 0, 0, 3, 0],  # Fri
    [0, 0, 0, 0, 0, 0, 5],  # Sat
    [1, 4, 0, 0, 0, 0, 0],  # Sun
]

# -----------------------------
# 2. Список ребер
# -----------------------------
edges = []
for i in range(n):
    for j in range(n):
        if adjacency_matrix[i][j] != 0:
            edges.append((vertices[i], vertices[j], adjacency_matrix[i][j]))

print("Список ребер:")
for i in edges:
    print(i)
# -----------------------------
# 3. Массив записей
# -----------------------------
vertex_records = []

for i, v in enumerate(vertices):
    parents = [vertices[j] for j in range(n) if adjacency_matrix[j][i] != 0]
    children = [vertices[j] for j in range(n) if adjacency_matrix[i][j] != 0]
    in_weights = [adjacency_matrix[j][i] for j in range(n) if adjacency_matrix[j][i] != 0]
    out_weights = [adjacency_matrix[i][j] for j in range(n) if adjacency_matrix[i][j] != 0]

    record = {
        "index": i,
        "name": v,
        "parents": parents,
        "children": children,
        "in_weights": in_weights,
        "out_weights": out_weights
    }
    vertex_records.append(record)

print("\nМассив записей (табличный вид):")
for rec in vertex_records:
    print(f"""
Вершина: {rec['name']} (индекс {rec['index']})
  Предки: {rec['parents']}
  Потомки: {rec['children']}
  Входящие веса: {rec['in_weights']}
  Исходящие веса: {rec['out_weights']}
""")

# -----------------------------
# 4. Визуализация графа
# -----------------------------
G = nx.DiGraph()
G.add_nodes_from(vertices)
G.add_weighted_edges_from(edges)

pos = nx.spring_layout(G)
plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue')
edge_labels = {(u, v): w for u, v, w in edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Ориентированный взвешенный граф")
plt.show()

# -----------------------------
# 5. Подпрограммы (12 штук)
# -----------------------------

# ===== МАТРИЦА СМЕЖНОСТИ =====

# Соседи вершины (без учета направления)
def neighbors_matrix(vertex_name):
    idx = vertices.index(vertex_name)
    return [vertices[j] for j in range(n)
            if adjacency_matrix[idx][j] != 0 or adjacency_matrix[j][idx] != 0]

# Проверка цепи (с учетом направления)
def is_chain_matrix(sequence):
    for i in range(len(sequence) - 1):
        if adjacency_matrix[vertices.index(sequence[i])][vertices.index(sequence[i + 1])] == 0:
            return False
    return True

# Вершины с суммой весов > threshold
def vertices_sum_matrix(threshold):
    result = []
    for i in range(n):
        total = sum(adjacency_matrix[i]) + sum(adjacency_matrix[j][i] for j in range(n))
        if total > threshold:
            result.append(vertices[i])
    return result

# Количество ребер
def count_edges_matrix():
    return sum(1 for row in adjacency_matrix for val in row if val != 0)


# ===== СПИСОК РЕБЕР =====

def neighbors_edges(vertex_name):
    result = set()
    for u, v, _ in edges:
        if u == vertex_name:
            result.add(v)
        elif v == vertex_name:
            result.add(u)
    return list(result)

def is_chain_edges(sequence):
    for i in range(len(sequence) - 1):
        if not any((u == sequence[i] and v == sequence[i + 1]) for u, v, _ in edges):
            return False
    return True

def vertices_sum_edges(threshold):
    result = []
    for v in vertices:
        total = sum(w for u1, v1, w in edges if u1 == v or v1 == v)
        if total > threshold:
            result.append(v)
    return result

def count_edges_list():
    return len(edges)


# ===== МАССИВ ЗАПИСЕЙ =====

def neighbors_records(vertex_name):
    for rec in vertex_records:
        if rec["name"] == vertex_name:
            return list(set(rec["parents"] + rec["children"]))
    return []

def is_chain_records(sequence):
    for i in range(len(sequence) - 1):
        current = next(rec for rec in vertex_records if rec["name"] == sequence[i])
        if sequence[i + 1] not in current["children"]:
            return False
    return True

def vertices_sum_records(threshold):
    result = []
    for rec in vertex_records:
        total = sum(rec["in_weights"]) + sum(rec["out_weights"])
        if total > threshold:
            result.append(rec["name"])
    return result

def count_edges_records():
    return sum(len(rec["out_weights"]) for rec in vertex_records)


# -----------------------------
# 6. Проверка работы функций
# -----------------------------
print("=== МАТРИЦА СМЕЖНОСТИ ===")
print("Соседи Mon:", neighbors_matrix("Mon"))
print("Цепь ['Mon','Thr']:", is_chain_matrix(["Mon", "Thr"]))
print("Вершины с суммой весов > 10:", vertices_sum_matrix(10))
print("Количество ребер:", count_edges_matrix())

print("\n=== СПИСОК РЕБЕР ===")
print("Соседи Tue:", neighbors_edges("Tue"))
print("Цепь ['Tue','Wed']:", is_chain_edges(["Tue", "Wed"]))
print("Вершины с суммой весов > 10:", vertices_sum_edges(10))
print("Количество ребер:", count_edges_list())

print("\n=== МАССИВ ЗАПИСЕЙ ===")
print("Соседи Fri:", neighbors_records("Fri"))
print("Цепь ['Fri','Wed']:", is_chain_records(["Fri", "Wed"]))
print("Вершины с суммой весов > 10:", vertices_sum_records(10))
print("Количество ребер:", count_edges_records())


# -----------------------------
# 7. Размер объектов
# -----------------------------
print("\nРазмер объектов в байтах:")
print("Матрица смежности:", sys.getsizeof(adjacency_matrix))
print("Список ребер:", sys.getsizeof(edges))
print("Массив записей:", sys.getsizeof(vertex_records))


# -----------------------------
# 8. Измерение времени
# -----------------------------
def measure_time(func, *args):
    repeat = 10 ** 5
    start = time.perf_counter()
    for _ in range(repeat):
        func(*args)
    end = time.perf_counter()
    return (end - start) / repeat


print("\n=== СРЕДНЕЕ ВРЕМЯ ВЫПОЛНЕНИЯ ===")

print("\n--- Матрица смежности ---")
print("neighbors:", measure_time(neighbors_matrix, "Mon"))
print("is_chain:", measure_time(is_chain_matrix, ["Mon", "Thr"]))
print("vertices_sum:", measure_time(vertices_sum_matrix, 10))
print("count_edges:", measure_time(count_edges_matrix))

print("\n--- Список ребер ---")
print("neighbors:", measure_time(neighbors_edges, "Mon"))
print("is_chain:", measure_time(is_chain_edges, ["Mon", "Thr"]))
print("vertices_sum:", measure_time(vertices_sum_edges, 10))
print("count_edges:", measure_time(count_edges_list))

print("\n--- Массив записей ---")
print("neighbors:", measure_time(neighbors_records, "Mon"))
print("is_chain:", measure_time(is_chain_records, ["Mon", "Thr"]))
print("vertices_sum:", measure_time(vertices_sum_records, 10))
print("count_edges:", measure_time(count_edges_records))