# coding=utf-8 
import copy
import sys
import math
import random
import utils
import time
import verify as vy

N = 20
T = 170
sampling_num = 10000
START_MAX_CHOICE = 5
START_MAX_ATTEMPT = 3
MAX_CHOICE = 15
MAX_ATTEMPT = 15
global CHOICES
THRESHOLD = 0.05


class State(object):

    def __init__(self, n, t):
        self.value = 0.0
        # self.board = [[0] * t for i in range(n)]
        self.verify_num = [0] * n
        self.round = 0
        self.choices = []
        self.is_full = False

    def new_state(self, temp_choices):
        global CHOICES
        state = State(N, T)
        state.value = self.value
        # state.board = copy.deepcopy(self.board)
        state.verify_num = copy.deepcopy(self.verify_num)
        # 随机在步骤池中选择一步
        ran = random.randint(0, len(temp_choices) - 1)
        choice = temp_choices[ran]
        flag = utils.judge_if_is_one(state.verify_num[choice[0]], choice[1], T)
        test = copy.deepcopy(state.verify_num)
        test_move_num = 1 << (T - choice[1])
        test[choice[0]] |= test_move_num
        # 判断棋盘行列是否已满
        flag = flag & utils.judge_if_row_full(test, N)
        # 如果不符合条件，重新进行随机
        while flag is False:
            ran = random.randint(0, len(temp_choices) - 1)
            choice = temp_choices[ran]
            test = copy.deepcopy(state.verify_num)
            test_move_num = 1 << (T - choice[1])
            test[choice[0]] |= test_move_num
            flag = utils.judge_if_is_one(state.verify_num[choice[0]], choice[1], T)
            flag = flag & utils.judge_if_row_full(test, N)
        choice = temp_choices.pop(ran)
        state.choices = self.choices + [choice]
        # state.board[choice[0]][choice[1]] = 1
        move_num = 1 << (T - choice[1])
        state.verify_num[choice[0]] |= move_num
        state.round = self.round + 1
        # 计算抽样可靠性
        verify = vy.Verify(N, T, sampling_num)
        state.value = verify.format_and_verify_sampling(state.verify_num) * 100
        return state

    def __repr__(self):
        return "State: {},, value: {}, choices: {}".format(
            hash(self), self.value, self.choices)


class Node(object):
    def __init__(self):
        self.parent = None
        self.children = []

        self.quality = 0.0
        self.visit = 0

        self.state = None

    def add_child(self, node):
        self.children.append(node)
        node.parent = self

    def __repr__(self):
        return "Node: {}, Q/N: {}/{}, state: {}".format(
            hash(self), self.quality, self.visit, self.state)


def expand(node, temp_choices):
    states = [nodes.state for nodes in node.children]
    state = node.state.new_state(temp_choices)

    while state in states:
        state = node.state.new_state(temp_choices)

    child_node = Node()
    child_node.state = state
    node.add_child(child_node)

    return child_node


# 选择， 扩展
def tree_policy(node, temp_choices):
    # 选择是否是叶子节点，
    if len(node.children) < MAX_CHOICE:
        node = expand(node, temp_choices)
        return node
    else:
        node = best_child(node)

    return node


# 模拟
def default_policy(node, temp_choices):
    now_state = node.state
    now_state = now_state.new_state(temp_choices)
    return now_state.value


def backup(node, reward):
    while node is not None:
        node.visit += 1
        node.quality += reward
        node = node.parent


def best_child(node):
    best_score = -sys.maxsize
    best = None

    for sub_node in node.children:

        C = 1 / math.sqrt(2.0)
        left = sub_node.quality / sub_node.visit
        right = 2.0 * math.log(node.visit) / sub_node.visit
        score = left + C * math.sqrt(right)

        if score > best_score:
            best = sub_node
            best_score = score

    return best


def mcts(node, best_value):
    global CHOICES
    # 每次模拟进行MAX_ATTEMPT次机会，取得比最好值更好的以后继续进行
    if node.state.value < 90.0:
        max_attempt = START_MAX_ATTEMPT
        max_choice = START_MAX_CHOICE
    else:
        max_attempt = MAX_ATTEMPT
        max_choice = MAX_CHOICE
    temp_choices = copy.deepcopy(CHOICES)
    for i in range(max_attempt):
        for j in range(max_choice):
            expand_node = tree_policy(node, temp_choices)
            reward = default_policy(expand_node, temp_choices)
            backup(expand_node, reward)
        best = best_child(node)
        print("%.4f" % best.state.value)
        if best.state.value > best_value or (best.state.value < best_value and best_value - best.state.value < THRESHOLD):
            break
        if i == MAX_ATTEMPT - 1:
            print("------round %d can't get a better answer--------" % best.state.round)
        else:
            print("------round %d find better answers failed,move to next attempt--------" % best.state.round)

    # 从CHOICES中去除最佳节点选择的步骤
    current_choice = best.state.choices[-1]
    for i in range(len(CHOICES) - 1):
        temp = CHOICES[i]
        if temp[0] == current_choice[0] and temp[1] == current_choice[1]:
            CHOICES.pop(i)

    print("------round %d finished expending and simulation, choosing best leaf node---------" % best.state.round)
    # for arr in best.state.verify_num:
    #     print((bin(arr)))
    print(best.state.choices)
    print("result: %.4f %%" % best.state.value)
    print("length of CHOICES: %d" % len(CHOICES))
    # print(utils.judge_if_row_full(utils.pos_format_matrix(N, T, best.state.choices), N))
    print("---------------------------------------------------------------------")

    return best


def main():
    start = time.time()
    global CHOICES
    CHOICES = []
    for x in range(N):
        for y in range(T):
            CHOICES.append([x, y])
    init_state = State(N, T)
    init_node = Node()
    init_node.state = init_state
    current_node = init_node

    best_round = 0
    best_value = 0.0
    # best_board = []
    best_verify_num = []
    best_choices = []
    previous_node = {}
    previous_value = {}
    # previous_board = {}
    previous_verify_num = {}
    previous_choices = {}
    return_round = {}

    while current_node.state.value < 99.0:
        # 存储之前的步骤
        previous_node[str(current_node.state.round)] = copy.deepcopy(current_node)
        previous_value[str(current_node.state.round)] = current_node.state.value
        previous_verify_num[str(current_node.state.round)] = copy.deepcopy(current_node.state.verify_num)
        previous_choices[str(current_node.state.round)] = copy.deepcopy(current_node.state.choices)

        current_node = mcts(current_node, best_value)

        if current_node.state.value > best_value:
            best_round = current_node.state.round
            best_value = current_node.state.value
            # best_board = copy.deepcopy(current_node.state.board)
            best_verify_num = copy.deepcopy(current_node.state.verify_num)
            best_choices = copy.deepcopy(current_node.state.choices)

        # 如果可靠率下降，差值超过给定阈值，启用回退策略
        # 回退步骤数目会随当前round回退次数递增
        base_return_num = 2
        if current_node.state.value < best_value and (best_value - current_node.state.value) > THRESHOLD:
            if return_round.get(str(current_node.state.round)) is None:
                return_round[str(current_node.state.round)] = 1
            else:
                return_round[str(current_node.state.round)] += 1
            return_num = base_return_num + return_round.get(str(current_node.state.round))
            
            print("-------round %d can't fit the demand, active rollback, rollback num%d----------" % (current_node.state.round, return_num))

            current_node.state.round -= return_num
            for i in range(return_num):
                choice = current_node.state.choices.pop()
                move_num = 1 << (T - choice[1])
                current_node.state.verify_num[choice[0]] &= ~move_num
                # current_node.state.board[choice[0]][choice[1]] = 0
                CHOICES.append(choice)

            if best_value < previous_value[str(current_node.state.round)] or best_round > current_node.state.round:
                best_value = previous_value[str(current_node.state.round)]
                # best_board = copy.deepcopy(previous_board[str(current_node.state.round)])
                best_verify_num = copy.deepcopy(previous_verify_num[str(current_node.state.round)])
                best_choices = copy.deepcopy(previous_choices[str(current_node.state.round)])
            current_node = copy.deepcopy(previous_node[str(current_node.state.round)])
            print("%.4f" % best_value)
            print("length of CHOICES: %d" % len(CHOICES))
            print("-------------finished rollback--------------")

    print("-----------------best result------------------")
    # for arr in best_verify_num:
    #     print(bin(arr))
    print(best_choices)
    print("sampling reliability: %.4f %%" % best_value)
    end = time.time()
    print('Running time: %s Seconds' % (end - start))
    print('Average round time: %.4f Seconds' % ((end - start) / best_round))


if __name__ == "__main__":
    main()
