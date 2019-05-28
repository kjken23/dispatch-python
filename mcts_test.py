import sys
import math
import random

MAX_CHOICE = 4
MAX_DEPTH = 50
CHOICES = [1, -1, 2, -2]

class State(object):
    def __init__(self):
        self.value = 0
        self.round = 0
        self.choices = []

    def new_state(self):
        choice = random.choice(CHOICES)
        state = State()
        state.value = self.value + choice
        state.round = self.round + 1
        state.choices = self.choices + [choice]

        return state

    def __repr__(self):
        return "State: {}, value: {}, choices: {}".format(
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
    while node.state.round < MAX_DEPTH:
        if len(node.children) < MAX_CHOICE:
            node = expand(node)
            return node
        else:
            node = best_child(node)

    return node

# 模拟
def default_policy(node):
    now_state = node.state
    while now_state.round < MAX_DEPTH:
        now_state = now_state.new_state()

    return now_state.value

def backup(node, reward):

    while node != None:
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

    times = 5
    for i in range(times):

        expand = tree_policy(node)
        reward = default_policy(expand)
        backup(expand, reward)

    best = best_child(node)

    return best

def main():
    init_state = State()
    init_node = Node()
    init_node.state = init_state
    current_node = init_node

    for i in range(MAX_DEPTH):
        a = 0.0
        b = 0.0
        c = 0.0
        d = 0.0
        current_node = mcts(current_node)

        for j in range(len(current_node.state.choices)):
            if current_node.state.choices[j] == -2:
                a += 1
            if current_node.state.choices[j] == -1:
                b += 1
            if current_node.state.choices[j] == 1:
                c += 1
            if current_node.state.choices[j] == 2:
                d += 1
        print("-2的概率为", round(a/(i + 1.0), 2),
              "-1的概率为", round(b/(i + 1.0), 2),
              "1的概率为", round(c/(i + 1.0), 2),
              "2的概率为", round(d/(i + 1.0), 2))

if __name__ == "__main__":
    main()