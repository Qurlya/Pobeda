adjacency_matrix = [
    [0, 3, 4, 0, 0, 0, 0],
    [3, 0, 5, 0, 0, 0, 0],
    [4, 5, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 1, 0],
    [0, 0, 0, 2, 0, 3, 0],
    [0, 0, 0, 1, 3, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]
k = 0
for i in range(len(adjacency_matrix)):
    for j in range(len(adjacency_matrix[i])):
        if j > i and adjacency_matrix[i][j] > 0:
            k+=1

incidence_matrix = [[0 for x in range(k)] for y in range(len(adjacency_matrix))]
for n in incidence_matrix:
    print(n)