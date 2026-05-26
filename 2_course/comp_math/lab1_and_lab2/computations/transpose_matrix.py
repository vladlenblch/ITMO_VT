def transpose(matrix):
    if isinstance(matrix, list) and (len(matrix) == 0 or not isinstance(matrix[0], list)):
        return [[x] for x in matrix]

    rows = len(matrix)
    cols = len(matrix[0])
    transposed_matrix = [[0 for _ in range(rows)] for _ in range(cols)]

    for i in range(rows):
        for j in range(cols):
            transposed_matrix[j][i] = matrix[i][j]

    return transposed_matrix
