def rotate_right(i, distance, t):
    right = i >> distance
    left = i << (t - distance)
    mask = (1 << t) - 1
    return (right | left) & mask


def list2str(array):
    return "".join([str(x) for x in array])


# def pos_format_matrix_str(n, t, array):
#     temp_matrix = [[0] * t for i in range(n)]
#     for arr in array:
#         temp_matrix[arr[0]][arr[1]] = 1
#     matrix = []
#     for i in range(len(temp_matrix)):
#         matrix.append(np.long(list2str(temp_matrix[i]), 2))
#     return matrix


# def format_matrix_long(array):
#     matrix = []
#     for i in range(len(array)):
#         matrix.append(np.long(list2str(array[i]), 2))
#     return matrix


def count(n):
    one_count = 0
    while n:
        one_count += 1
        # 把一个整数减去1，再和原整数做与运算，会把该整数最右边的一个1变成0
        # 有多少个1就能进行多少次转化
        n = n & (n - 1)
    return one_count


def judge_if_row_full(array, n):
    for i in array:
        if count(i) > n:
            return False
    return True


def judge_if_col_full(choice, array, n):
    y = choice[1]
    col_count = 0
    for arr in array:
        if arr[y] == 1:
            col_count += 1
    return col_count < n / 3


# 判断数字n的第i位（从左往右）是否为1
def judge_if_is_one(n, i, t):
    return n >> (t - i) & 1 != 1
