import copy
import random

import utils


def judge_single_node(array_list, i, n, t):
    mask = (1 << t) - 1
    others = 0

    for j in range(n):
        if j == i:
            continue
        others = others | array_list[j]
    return (array_list[i] & mask) & (~others & mask) > 0


class Verify(object):

    def __init__(self, n, t, sampling_num):
        self.n = n
        self.t = t
        self.samplingNum = sampling_num

    def judge(self, array_list, count_map):
        for i in range(len(array_list)):
            if judge_single_node(array_list, i, self.n, self.t):
                count_map[i] = count_map[i] + 1

    def sampling_verify(self, array_list, count_map, sampling_num):
        temp = copy.deepcopy(array_list)
        for i in range(len(array_list)):
            count_map[i] = 0

        for i in range(sampling_num):
            for j in range(len(array_list)):
                offset = random.randint(0, self.t)
                temp[j] = utils.rotate_right(temp[j], offset, self.t)
            self.judge(temp, count_map)

        count = 0
        for (k,v) in count_map.items():
            count += v

        return count / (len(array_list) * sampling_num)

    def format_and_verify_sampling(self, array_list):
        count_map = dict()
        result = self.sampling_verify(array_list, count_map, self.samplingNum)
        # print("抽样可靠率： %.6f" % result)
        return result
