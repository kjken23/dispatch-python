import copy
import sys
import math
import random
import utils
import verify as vy

N = 10
T = 63
sampling_num = 10000
MAX_CHOICE = 15
MAX_ATTEMPT = 10
CHOICES = []
BASE = 0.95


class State(object):
    def __init__(self, n, t):
        self.value = 0.0
        self.board = [[0] * t for i in range(n)]
        self.round = 0
        self.choices = []
        self.is_full = False

    def new_state(self):
        state = State(N, T)
        state.value = self.value
        state.board = copy.deepcopy(self.board)
        # 随机在步骤池中选择一步
        ran = random.randint(0, len(CHOICES) - 1)
        temp_choice = copy.deepcopy(CHOICES)
        choice = temp_choice[ran]
        flag = state.board[choice[0]][choice[1]] != 1
        test = copy.deepcopy(state.board)
        test[choice[0]][choice[1]] = 1
        # 判断棋盘行列是否已满
        flag = flag & utils.judge_if_row_full(test, N)
        flag = flag & utils.judge_if_col_full(choice, test, N)
        # 如果不符合条件，重新进行随机
        while flag is False:
            ran = random.randint(0, len(CHOICES) - 1)
            choice = CHOICES[ran]
            test = copy.deepcopy(state.board)
            test[choice[0]][choice[1]] = 1
            flag = state.board[choice[0]][choice[1]] != 1
            flag = flag & utils.judge_if_row_full(test, N)
            flag = flag & utils.judge_if_col_full(choice, test, N)
        choice = temp_choice.pop(ran)
        state.choices = self.choices + [choice]
        state.board[choice[0]][choice[1]] = 1
        state.round = self.round + 1
        # state.is_full = utils.board_full(state.board, N)
        # if state.is_full:
        # 计算抽样可靠性
        verify = vy.Verify(N, T, sampling_num)
        state.value = verify.format_and_verify_sampling(state.board) * 100
        return state

    def __repr__(self):
        return "State: {}, board: {}, value: {}, choices: {}".format(
            hash(self), self.board, self.value, self.choices)


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


def expand(node):
    states = [nodes.state for nodes in node.children]
    state = node.state.new_state()

    while state in states:
        state = node.state.new_state()

    child_node = Node()
    child_node.state = state
    node.add_child(child_node)

    return child_node


# 选择， 扩展
def tree_policy(node):
    # 选择是否是叶子节点，
    # while node.state.is_full is False:
    if len(node.children) < MAX_CHOICE:
        node = expand(node)
        return node
    else:
        node = best_child(node)

    return node


# 模拟
def default_policy(node):
    now_state = node.state
    # while now_state.is_full is False:
    now_state = now_state.new_state()
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
    # 每次模拟进行MAX_ATTEMPT次机会，取得比最好值更好的以后继续进行
    for i in range(MAX_ATTEMPT):
        for j in range(MAX_CHOICE):
            expand_node = tree_policy(node)
            reward = default_policy(expand_node)
            backup(expand_node, reward)
        best = best_child(node)
        if best.state.value > best_value:
            break
        if i == MAX_ATTEMPT - 1:
            print("------round %d 当前未搜索到更优解，进入下一层--------" % best.state.round)

    print("------round %d 完成扩展和模拟，进行最佳叶子节点选择---------" % best.state.round)
    for arr in best.state.board:
        print(arr)
    print(best.state.choices)
    print("result: %.4f %%" % best.state.value)
    # print(utils.judge_if_row_full(utils.pos_format_matrix(N, T, best.state.choices), N))
    print("---------------------------------------------------------------------")

    return best


def main():
    for x in range(N):
        for y in range(T):
            CHOICES.append([x, y])
    init_state = State(N, T)
    init_node = Node()
    init_node.state = init_state
    current_node = init_node

    best_value = 0.0
    best_board = []
    best_choices = []
    previous_value = {'1': 0.0, '2': 0.0, '3': 0.0}
    previous_board = {'1': [], '2': [], '3': []}
    previous_choices = {'1': [], '2': [], '3': []}

    while current_node.state.round < (N * N) / 2:
        # 存储之前的步骤
        if current_node.state.round > 3:
            previous_value['3'] = previous_value['2']
            previous_board['3'] = copy.deepcopy(previous_board['2'])
            previous_choices['3'] = copy.deepcopy(previous_choices['2'])

        if current_node.state.round > 2:
            previous_value['2'] = previous_value['1']
            previous_board['2'] = copy.deepcopy(previous_board['1'])
            previous_choices['2'] = copy.deepcopy(previous_choices['1'])

        if current_node.state.round > 1:
            previous_value['1'] = current_node.state.value
            previous_board['1'] = copy.deepcopy(current_node.state.board)
            previous_choices['1'] = copy.deepcopy(current_node.state.choices)

        current_node = mcts(current_node, best_value)

        if current_node.state.value > best_value:
            best_value = current_node.state.value
            best_board = copy.deepcopy(current_node.state.board)
            best_choices = copy.deepcopy(current_node.state.choices)

        # 如果可靠率下降，超过最佳值0.1%，启用回退策略
        if current_node.state.value < best_value and (best_value - current_node.state.value) > 0.1:
            print("-------round %d 未达到要求，启用回退策略----------" % current_node.state.round)
            return_num = 3
            return_choice = []
            current_node.state.round -= 3
            for i in range(return_num):
                return_choice += [current_node.state.choices.pop()]
            for choice in return_choice:
                current_node.state.board[choice[0]][choice[1]] = 1
            best_value = previous_value['3']
            best_board = previous_board['3']
            best_choices = previous_choices['3']
            print("----------完成回退--------------")

    print("-----------------result------------------")
    for arr in best_board:
        print(arr)
    print(best_choices)
    print("抽样可靠率: %.4f %%" % best_value)


if __name__ == "__main__":
    main()
