import random
import numpy as np
import matplotlib.pyplot as plt

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree


class GraphNode:
    def __init__(self, global_node_id, u_from_parent, parent_global_node_id):
        self.global_node_id = global_node_id
        self.u_from_parent = u_from_parent
        self.parent_global_node_id = parent_global_node_id

    def __str__(self):
        return f"id: {self.global_node_id}, u from parent: {self.u_from_parent}, parent id: {self.parent_global_node_id}"


class Graph:
    def __init__(self):
        self.nodes_dict = {}  # {node_global_id: GraphNode}
        self.recognition_order = []  # [node_global_id_1, ..., node_global_id_n]

    def get_parent_id(self, child_id):
        graph_node = self.nodes_dict[child_id]
        return graph_node.parent_global_node_id

    @staticmethod
    def rand_point():
        X = random.randint(0, 50)
        Y = random.randint(0, 50)
        return np.array((X, Y))

    @staticmethod
    def get_shift(point_1, point_2):
        shift = point_2 - point_1
        return shift

    def show_graph(self):
        X = []
        Y = []
        points = []
        for i in range(len(self.recognition_order)):
            points.append(self.rand_point())

        for point in points:
            X.append(point[0])
            Y.append(point[1])

        plt.plot(X, Y, 'o', color="red")

        for i in range(len(self.recognition_order)):
            plt.text(X[i] + 0.35, Y[i] + 0.35, self.recognition_order[i], color="red")

        for i in range(1, len(self.recognition_order)):
            point_1_id = self.nodes_dict[self.recognition_order[i]].parent_global_node_id
            point_2_id = self.nodes_dict[self.recognition_order[i]].global_node_id

            index_1 = self.recognition_order.index(point_1_id)
            index_2 = self.recognition_order.index(point_2_id)

            shift_x, shift_y = self.get_shift(points[index_1], points[index_2])

            plt.arrow(x=X[index_1], y=Y[index_1], dx=shift_x, dy=shift_y, width=0.2,
                      length_includes_head=True, color="black")

        plt.show()


def get_root(tree):
    roots = []
    for i in range(len(tree[0])):
        count = 0
        for j in range(len(tree)):
            if tree[j][i] == 0:
                count += 1
        if count == len(tree):
            roots.append(i)
    return roots


def get_children(tree, node):
    children = []
    for i in range(len(tree[node])):
        if tree[node][i] != 0:
            children.append(i)

    return children


def get_parent(tree, node):
    for i in range(len(tree[node])):
        if tree[i][node] != 0:
            return i
    return None


def get_du_from_parent(tree, node):
    for i in range(len(tree[node])):
        if tree[i][node] != 0:
            return tree[i][node]
    return None


def traverse(tree, node, path=None):
    if path is None:
        path = []

    path.append(node)

    for node in get_children(tree, node):
        traverse(tree, node, path)

    return path


def get_leaves(matrix):
    leaves = []
    roots = get_root(matrix)
    for i in range(len(matrix)):
        num_zeros = len(matrix[i][np.where(matrix[i] == 0)])
        if num_zeros == len(matrix) - 1 and i in roots:
            leaves.append(i)
    return leaves


def transpose_row(matrix, index):
    tmp_row = matrix[index]

    for i in range(len(matrix)):
        tmp_col_el = matrix[i][index]
        matrix[i][index] = tmp_row[i]
        matrix[index][i] = tmp_col_el

    return matrix


def get_oriented_mat(matrix):
    leaves = get_leaves(matrix)
    for leaf in leaves:
        matrix = transpose_row(matrix, leaf)

    return matrix


def get_optimized_graph(adjacency_matrix, id_list):
    Tcsr = minimum_spanning_tree(adjacency_matrix)
    min_tree = Tcsr.toarray().astype(float)

    if len(min_tree[0]) != len(id_list):
        print("Amount of ids don't match with adjacency matrix!")
        return None

    else:
        roots = get_root(min_tree)

        if len(roots) > 1:
            min_tree = get_oriented_mat(min_tree)
            roots = get_root(min_tree)

        root = roots[0]

        order = traverse(min_tree, root)

        graph_nodes = []
        for i in range(len(id_list)):
            du = get_du_from_parent(min_tree, i)
            parent_ind = get_parent(min_tree, i)

            if parent_ind is None:
                graph_nodes.append(GraphNode(id_list[i], du, None))
            else:
                graph_nodes.append(GraphNode(id_list[i], du, id_list[parent_ind]))

        path = Graph()
        for node_id in order:
            path.recognition_order.append(id_list[node_id])

        for node in graph_nodes:
            path.nodes_dict[node.global_node_id] = node

        return path


