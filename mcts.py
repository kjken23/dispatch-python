import copy
import sys
import math
import random
import utils
import verify as vy

N = 10
T = 63
sampling_num = 10000
MAX_CHOICE = 10
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
        ran = random.randint(0, len(CHOICES) - 1)
        temp_choice = copy.deepcopy(CHOICES)
        choice = temp_choice[ran]
        flag = state.board[choice[0]][choice[1]] != 1
        test = copy.deepcopy(state.board)
        test[choice[0]][choice[1]] = 1
        flag = flag & utils.judge_if_row_full(test, N)
        # flag = flag & utils.judge_if_col_full(choice, test, N)
        while flag is False:
            ran = random.randint(0, len(CHOICES) - 1)
            choice = CHOICES[ran]
            test = copy.deepcopy(state.board)
            test[choice[0]][choice[1]] = 1
            flag = state.board[choice[0]][choice[1]] != 1
            flag = flag & utils.judge_if_row_full(test, N)
            # flag = flag & utils.judge_if_col_full(choice, test, N)
        choice = temp_choice.pop(ran)
        state.choices = self.choices + [choice]
        state.board[choice[0]][choice[1]] = 1
        state.round = self.round + 1
        # state.is_full = utils.board_full(state.board, N)
        # if state.is_full:
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


def mcts(node):
    for i in range(MAX_CHOICE):
        expand_node = tree_policy(node)
        reward = default_policy(expand_node)
        backup(expand_node, reward)

    best = best_child(node)
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
    while current_node.state.round < N * N - 1:
        current_node = mcts(current_node)
        if current_node.state.value > best_value:
            best_value = current_node.state.value
            best_board = copy.deepcopy(current_node.state.board)
            best_choices = copy.deepcopy(current_node.state.choices)

    print("-----------------result------------------")
    for arr in best_board:
        print(arr)
    print(best_choices)
    print("抽样可靠率: %.4f %%" % best_value)


if __name__ == "__main__":
    main()
