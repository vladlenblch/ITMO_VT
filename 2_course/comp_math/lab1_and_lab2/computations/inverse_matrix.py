def inverse_2_by_2(matrix):
    adj_matrix = [
        [matrix[1][1], -matrix[0][1]],
        [-matrix[1][0], matrix[0][0]],
    ]
    det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    inverted_matrix = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            inverted_matrix[i][j] = adj_matrix[i][j] / det

    return inverted_matrix
