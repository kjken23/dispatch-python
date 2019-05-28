import numpy as np


# 循环移动数组k位，左移为正，右移为负
def move_array_element(array, k):
    return array[k:] + array[:k]


def rotate_right(i, distance, t):
    right = np.long(i >> distance)
    left = np.long(i << (t - distance))
    mask = np.long((np.long(1) << t) - np.long(1))
    return (right | left) & mask


def list2str(array):
    return "".join([str(x) for x in array])


def format_matrix(n, t, array):
    temp_matrix = [[0] * t for i in range(n)]
    for x in temp_matrix:
        x[0] = 1
    for i in range(len(array)):
        pos = 1
        for j in array[i]:
            pos += j
            temp_matrix[i][pos % t] = 1
            pos += 1
    matrix = []
    for i in range(len(array)):
        matrix.append(np.long(list2str(temp_matrix[i]), 2))
    return matrix


def pos_format_matrix(n, t, array):
    temp_matrix = [[0] * t for i in range(n)]
    for arr in array:
        temp_matrix[arr[0]][arr[1]] = 1
    matrix = []
    return matrix


def pos_format_matrix_str(n, t, array):
    temp_matrix = [[0] * t for i in range(n)]
    for arr in array:
        temp_matrix[arr[0]][arr[1]] = 1
    matrix = []
    for i in range(len(temp_matrix)):
        matrix.append(np.long(list2str(temp_matrix[i]), 2))
    return matrix


def format_matrix_long(array):
    matrix = []
    for i in range(len(array)):
        matrix.append(np.long(list2str(array[i]), 2))
    return matrix


def count(n):
    one_count = 0
    # 负数与0xffffffff相与，消除死循环
    if n < 0:
        n = n & 0xffffffff
    while n:
        one_count += 1
        # 把一个整数减去1，再和原整数做与运算，会把该整数最右边的一个1变成0
        # 有多少个1就能进行多少次转化
        n = n & (n - 1)
    return one_count


def board_full(array, n):
    for i in array:
        if count(np.long(list2str(i), 2)) < n:
            return False
    return True


def judge_if_row_full(array, n):
    for i in array:
        if count(np.long(list2str(i), 2)) > n:
            return False
    return True


def judge_if_col_full(choice, array, n):
    y = choice[1]
    col_count = 0
    for arr in array:
        if arr[y] == 1:
            col_count += 1
    return col_count < n / 2
