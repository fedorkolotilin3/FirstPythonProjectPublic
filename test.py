A = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
S = A[0][1]
for i in range(3):
    for j in range(i + 1, 3):
        print(A[i][j])
        S += A[i][j]