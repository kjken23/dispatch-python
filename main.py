import verify as vy

# array_list = [[0, 14, 11, 1, 1, 1, 8], [1, 3, 4, 5, 3, 8, 12], [1, 2, 18, 4, 4, 2, 5], [0, 1, 4, 4, 14, 2, 11], [0, 2, 6, 2, 6, 10, 10], [0, 4, 12, 6, 3, 4, 7], [0, 1, 13, 7, 1, 6, 8]]
array_list = [[6, 53], [7, 41], [7, 56], [9, 17], [9, 15], [9, 38], [6, 57], [8, 14], [8, 57], [0, 41], [2, 12], [8, 59], [5, 49], [1, 3], [1, 35], [6, 16], [6, 41], [3, 35], [3, 32], [3, 46], [1, 25], [1, 2], [8, 23], [0, 53], [1, 28], [0, 42], [4, 14], [3, 39], [1, 39], [2, 28], [0, 21], [5, 9], [5, 23], [7, 10], [0, 5], [0, 21], [2, 25], [4, 9], [9, 32], [2, 41], [0, 14], [7, 15], [9, 1], [5, 5], [2, 46], [8, 7], [3, 53], [2, 54], [2, 45], [2, 46], [2, 43], [0, 10], [5, 14], [1, 34], [8, 53], [9, 10], [6, 45], [1, 52], [2, 62], [4, 60], [6, 52], [2, 33], [8, 14], [8, 49], [3, 42], [3, 33], [9, 32], [9, 6], [0, 42], [7, 12], [7, 11], [8, 32], [3, 47], [6, 14], [6, 50], [7, 2], [7, 11], [3, 29], [2, 54], [7, 12], [7, 54], [3, 57], [9, 11], [8, 42], [2, 45], [0, 43], [4, 23], [7, 2], [4, 6], [9, 42], [0, 33], [8, 4], [6, 10], [0, 58], [6, 38], [4, 20], [7, 32], [7, 44], [9, 19], [1, 10]]
n = 7
t = 43
sampling_num = 10000

if __name__ == '__main__':
    verify = vy.Verify(n, t, sampling_num)
    result = verify.pos_format_and_verify_sampling(array_list)
    print("result: %.6f" % result)