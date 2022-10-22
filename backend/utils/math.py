def transpose(A):
    B = [[0 for a in range(len(A))] for a in range(len(A[0]))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            B[j][i] = A[i][j]
    return B


def mulMatrix(A, B):
    if len(A[0]) != len(B):
        return []
    C = [[0 for a in range(len(A))] for a in range(len(B[0]))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            s = 0
            for k in range(len(A[0])):
                s += A[i][k] * B[k][j]
            C[i][j] = s
    return C
