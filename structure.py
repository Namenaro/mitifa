from hists import Hist

class Node:
    def __init__(self, global_node_id, u_from_parent, parent_global_node_id, mass, LUE_id):
        # поля, нужные для процесса распознавания
        self.global_node_id = global_node_id
        self.u_from_parent = u_from_parent
        self.parent_global_node_id = parent_global_node_id
        self.mass = mass
        self.LUE_id = LUE_id

        # поля, нужные для расчетов нетривиальности
        self.actual_m_hist = None  #Hist
        self.actual_du_hist = None  #Hist

    def eval_nontriviality_of_event(self, real_mass, real_du_len):
        probability_of_dm = self.actual_m_hist.get_probability_of_event(real_value=real_mass, predicted_value=self.mass)
        probability_of_du = self.actual_du_hist.get_probability_of_event(real_value=real_du_len, predicted_value=0)
        return (1-probability_of_dm) + (1-probability_of_du)


class Structure:
    def __init__(self):
        self.nodes_dict = {}  # {node_global_id: Node}
        self.recognition_order = []  # [node_global_id_1, ..., node_global_id_n]

        self.basic_nodes_ids = set()
        self.non_basic_nodes_ids = set()


    def get_info_to_recognise_node(self, global_node_id):
        node = self.nodes_dict[global_node_id]
        return node.parent_global_node_id, node.u_from_parent, node.mass, node.LUE_id

    def event_is_basic(self, global_node_id):
        if global_node_id in self.basic_nodes_ids:
            return True
        return False

    def add_node(self, global_node_id, u_from_parent, parent_global_node_id, mass, LUE_id, actual_m_hist=None, actual_du_hist=None):
        new_node = Node(global_node_id, u_from_parent, parent_global_node_id, mass, LUE_id)
        self.nodes_dict[global_node_id]=new_node
        self.recognition_order.append(global_node_id)
        if actual_m_hist is None:
            self.non_basic_nodes_ids.append(global_node_id)
        else:
            self.basic_nodes_ids.append(global_node_id)
            self.nodes_dict[global_node_id].actual_m_hist = actual_m_hist
            self.nodes_dict[global_node_id].actual_du_hist = actual_du_hist


    def get_first_global_event_id(self):
        return self.recognition_order[0]

    def get_node_by_global_id(self, global_event_id):
        return self.nodes_dict.get(global_event_id, None)

    def is_empty(self):
        return len(self.nodes_dict)==0

    def get_mass(self, global_event_id):
        return self.get_node_by_global_id(global_event_id).mass

