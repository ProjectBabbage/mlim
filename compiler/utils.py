from compiler import model


def transpose(A: model.Matrix):
    size = A.getSize()
    B = [[0 for a in range(size[0])] for a in range(size[1])]
    for i in range(size[0]):
        for j in range(size[1]):
            B[j][i] = A.operand[i][j]
    return model.Matrix(B)


def mulMatrix(A: model.Matrix, B: model.Matrix):
    sizeA = A.getSize()
    sizeB = B.getSize()
    if sizeA[1] != sizeB[0]:
        return []
    C = [[0 for a in range(sizeA[0])] for a in range(sizeB[1])]
    for i in range(sizeA[0]):
        for j in range(sizeB[1]):
            s = model.Value(0)
            for k in range(sizeA[1]):
                s += A.operand[i][k] * B.operand[k][j]
            C[i][j] = s
    return model.Matrix(C)


def mulMatrixbyScalar(A: model.Matrix, b: model.Value):
    for i in range(A.getSize()[0]):
        for j in range(A.getSize()[1]):
            A.operand[i][j] = b * A.operand[i][j]
    return model.Matrix(A)


def divMatrixbyScalar(A: model.Matrix, b: model.Value):
    for i in range(A.getSize()[0]):
        for j in range(A.getSize()[1]):
            A.operand[i][j] = A.operand[i][j] / b
    return A


def subMatrix(A: model.Matrix, B: model.Matrix):
    size = A.getSize()
    if size[1] != B.getSize[1] or size[0] != B.getSize[0]:
        return []
    for i in range(size[0]):
        for j in range(size[1]):
            A.operand[i][j] -= B.operand[i][j]
    return A


def addMatrix(A: model.Matrix, B: model.Matrix):
    size = A.getSize()
    if len(size[1]) != len(B.getSize()[1]) or len(size[0]) != len(B.getSize()[0]):
        return []
    for i in range(size[0]):
        for j in range(size[1]):
            A.operand[i][j] += B.operand[i][j]
    return A


def selectElement(A: model.Matrix, i: model.Value, j: model.Value):
    i = int(i.operand) - 1
    j = int(j.operand) - 1
    return A.operand[i][j]
