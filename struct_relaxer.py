from structure import *
from exemplar import *
from graph_optimisation import *
from sampler import *
from utils import *

import numpy as np

class StructRelaxer:
    def __init__(self, basic_struct, context):
        self.basic_struct = basic_struct
        self.context = context

    def get_relaxed_dammy_struct(self):

        exemplars = sample_struct(self.context.train_maps, basic_struct=self.basic_struct)

        matrix_dispersions, matrix_u_points, list_events_ids = self.exemplars_to_means_u_and_dist_dispersions(exemplars)
        graph = get_optimized_graph(matrix_dispersions, list_events_ids)

        # оптимизированный граф превращаем в dammy_struct
        dammy_struct = Structure()

        first_global_node_id = graph.recognition_order[0]
        _, _, mass, LUE_id = self.basic_struct.get_info_to_recognise_node(first_global_node_id)
        dammy_struct.add_node(global_node_id=first_global_node_id, u_from_parent=None, parent_global_node_id=None, mass=mass, LUE_id=LUE_id)

        for global_node_id in graph.recognition_order[1:]:
            _, _, mass, LUE_id = self.basic_struct.get_info_to_recognise_node(global_node_id)
            parent_global_node_id = graph.get_parent_id(global_node_id)
            u_from_parent = self.get_u_btw_2_nodes(node_start_id=parent_global_node_id, node_end_id=global_node_id, matrix_u=matrix_u_points, ids_ordered_list=list_events_ids)
            dammy_struct.add_node(global_node_id=global_node_id, u_from_parent=u_from_parent, parent_global_node_id=parent_global_node_id,
                                  mass=mass, LUE_id=LUE_id)
        return dammy_struct

    def get_u_btw_2_nodes(self, node_start_id, node_end_id, matrix_u, ids_ordered_list):
        index_i = ids_ordered_list.index(node_start_id)
        index_j = ids_ordered_list.index(node_end_id)
        return matrix_u[index_i][index_j]

    def get_mean_u_and_dists_dispersion(self, sample_x, sample_y):
        mean_x = np.mean(sample_x)
        mean_y = np.mean(sample_y)

        for i in range(len(sample_x)):
            sample_x[i] -= mean_x
            sample_y[i] -= mean_y
        sample_dists = []
        for i in range(len(sample_x)):
            sample_dists.append(norm(Point(sample_x[i], sample_y[i])))

        mean_u = Point(mean_x, mean_y)
        return mean_u, np.std(sample_dists)

    def exemplars_to_means_u_and_dist_dispersions(self, exemplars):
        result_matrix_dispersions = []
        result_matrix_us = []

        structure = exemplars[0].structure
        for start_node_id in structure.recognition_order:
            us_array, dispersions_array_for_this_start_node = self.get_all_data_for_node(exemplars, start_node_id, structure.recognition_order)
            result_matrix_dispersions.append(dispersions_array_for_this_start_node)
            result_matrix_us.append(us_array)

        return result_matrix_dispersions, result_matrix_us, structure.recognition_order

    def get_all_data_for_node(self, exemplars, start_node_id, nodes_ids_list):
        samples_list_x = list([[] for _ in range(len(nodes_ids_list))])
        samples_list_y = list([[] for _ in range(len(nodes_ids_list))])
        for exemplar in exemplars:
            start_point = exemplar.get_point_by_global_node_id(self, start_node_id)
            for i in range(len(nodes_ids_list)):
                end_node_id = nodes_ids_list[i]
                end_point = exemplar.get_point_by_global_node_id(self, end_node_id)
                x = end_point.x - start_point.x
                y = end_point.y - start_point.y
                samples_list_x[i].append(x)
                samples_list_y[i].append(y)
        us_array = []
        dist_dispersions_array = []
        for i in range(len(nodes_ids_list)):
            mean_u, std = self.get_mean_u_and_dists_dispersion(samples_list_x[i], samples_list_y[i])
            dist_dispersions_array.append(std)
            us_array.append(mean_u)
        return us_array, dist_dispersions_array





