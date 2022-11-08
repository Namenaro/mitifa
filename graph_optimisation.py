# Илья

def get_optimized_graph(ajacency_matrix, nodes_ids_list):
    return Graph

class GraphNode:
    def __init__(self, global_node_id, weight, parent_global_node_id):
        self.global_node_id = global_node_id
        self.weight = weight
        self.parent_global_node_id = parent_global_node_id


class Graph:
    def __init__(self):
        self.nodes_dict = {}  # {node_global_id: GraphNode}
        self.recognition_order = []  # [node_global_id_1, ..., node_global_id_n]

    def get_parent_id(self, child_id):
        return self.nodes_dict[child_id].parent_global_node_id


