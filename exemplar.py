from structure import *
from hists import *
from utils import norm, Point

from copy import deepcopy


class NodeRecognitionRes:
    def __init__(self, structure_node):
        self.structure_node = structure_node
        self.mass = None
        self.du = None  # Point, ошибка по отношению к предсказанному
        self.point = None

    def eval_m_probability(self):
        if self.structure_node.actual_m_hist is None:
            return None
        predicted_mass = self.structure_node.mass
        probability = self.structure_node.actual_m_hist.get_probability_of_event(real_value=self.mass, predicted_value=predicted_mass)
        return probability

    def eval_du_probability(self):
        if self.structure_node.actual_du_hist is None:
            return None
        predicted_du = 0
        real_du = norm(self.du)
        probability = self.structure_node.actual_m_hist.get_probability_of_event(real_value=real_du, predicted_value=predicted_du)
        return probability

class Exemplar:
    def __init__(self, structure, cogmap):
        self.structure = structure
        self.cogmap = cogmap

        self.nodes_local_ids = {}  # {global_node_id: node_local_id }

        self.next_index_to_recognise = 0   # индекс в Structure.recognition_order
        self.list_basic_nodes_ids_to_recognise = deepcopy(structure.basic_nodes_ids)
        self.list_non_basic_nodes_ids_to_recognise = deepcopy(structure.non_basic_nodes_ids)

        self.nodes_recognition_results = {}  # {global_node_id: NodeRecognitionRes }

    def get_global_id_by_local_id(self, local_id):
        for global_node_id, node_local_id in self.nodes_local_ids.items():
            if node_local_id == local_id:
                return global_node_id
        return None

    def __len__(self):
        return len(self.nodes_recognition_results)
    def eval_exemplar(self):
        exemplar_non_triviality = 0
        for global_node_id, node_recognition_res in self.nodes_recognition_results.items():
            mass_probability = node_recognition_res.eval_m_probability()
            du_probability = node_recognition_res.eval_du_probability()

            exemplar_non_triviality += mass_probability
            exemplar_non_triviality += du_probability
        return exemplar_non_triviality

    def add_event_check_result(self, global_node_id, local_cogmap_id):
        # обновляем сведения о том, что распознано, а что еще нет
        if self.structure.event_is_basic(global_node_id):
            self.list_basic_nodes_ids_to_recognise.remove(global_node_id)
        else:
            self.list_non_basic_nodes_ids_to_recognise.remove(global_node_id)

        self.add_event_check_result_DAMMY(global_node_id, local_cogmap_id)

    def add_event_check_result_DAMMY(self, global_node_id, local_cogmap_id):
        self.nodes_local_ids[global_node_id] = local_cogmap_id
        self.next_index_to_recognise += 1

        structure_node = self.structure.get_node_by_global_id(global_node_id)
        node_recognition_res = NodeRecognitionRes(structure_node)
        point, mass, _ = self.cogmap.get_event_data(local_cogmap_id)
        node_recognition_res.structure_node = structure_node
        node_recognition_res.mass = mass
        node_recognition_res.point = point
        parent_node_global_id = structure_node.parent_global_node_id

        # заполняем du:
        if parent_node_global_id is not None:
            parent_point = self.nodes_recognition_results[parent_node_global_id].point
            predicted_point = parent_point + structure_node.u_from_parent
            node_recognition_res.du = point - predicted_point
        else:
            # это первая нода в цепочке # TODO возможно du надо ставить наоборот максимальным??
            node_recognition_res.du = Point(0,0)

        # добавляем новое событие
        self.nodes_recognition_results[global_node_id] = node_recognition_res
    def make_prediction_for_next_event(self):
        next_global_node_id = self.get_next_event_global_id()
        parent_global_id, u_from_parent, predicted_mass, predicted_LUE_id =\
            self.structure.get_info_to_recognise_node(next_global_node_id)
        parent_event_point = self.get_point_by_global_node_id(parent_global_id)
        predicted_point = parent_event_point + u_from_parent
        return next_global_node_id, predicted_point, predicted_mass, predicted_LUE_id

    def is_basic_recognition_done(self):
        if len(self.list_basic_nodes_ids_to_recognise)==0:
            return True
        return False

    def is_recognition_done(self):
        if self.is_basic_recognition_done() and len(self.list_non_basic_nodes_ids_to_recognise) == 0:
            return True
        return False

    def get_no_more_MAX_events_around_point_by_LUE(self, point, predicted_LUE_id, MAX):
        # причем событий-кандидатов проверяем, не учтено ли оно уже в этом экземпляре
        already_recognised_local_ids = list(self.nodes_local_ids.values())
        local_evends_ids_list = self.cogmap.get_no_more_events_around_point_by_LUE(point, predicted_LUE_id,
                                                                                   MAX_EVENTS=MAX, exclusions=already_recognised_local_ids)
        return local_evends_ids_list

    def get_next_event_global_id(self):
        if self.is_recognition_done():
            return None
        global_node_id = self.structure.recognition_order[self.next_index_to_recognise]
        return global_node_id

    def get_point_by_global_node_id(self, global_node_id):
        return self.nodes_recognition_results[global_node_id].point

    def get_node_recognition_res(self, global_node_id):
        return self.nodes_recognition_results[global_node_id]













