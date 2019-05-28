import copy
import random
import numpy as np

import utils


class Verify(object):

    def __init__(self, n, t, sampling_num):
        self.n = n
        self.t = t
        self.samplingNum = sampling_num

    def judge_single_node(self, array_list, i):
        mask = np.long((np.long(1) << self.t) - np.long(1))
        others = np.long(0)
        for j in range(self.n):
            if j == i:
                continue
            others = np.long(others | array_list[j])
        return np.long(np.long(array_list[i] & mask) & np.long(~others & mask)) > np.long(0)

    def judge(self, array_list, count_map):
        for i in range(len(array_list)):
            if self.judge_single_node(array_list, i):
                count_map[i] = count_map[i] + 1

    def sampling_verify(self, array_list, count_map, sampling_num):
        temp = copy.copy(array_list)
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
        result = self.sampling_verify(utils.format_matrix_long(array_list), count_map, self.samplingNum)
    # print("抽样可靠率： %.6f" % result)
        return result

    def pos_format_and_verify_sampling(self, array_list):
        count_map = dict()
        result = self.sampling_verify(utils.pos_format_matrix_str(10, 63, array_list), count_map, self.samplingNum)
        # print("抽样可靠率： %.6f" % result)
        return result