from structure import *
from exemplar import *
from context import *
from cogmap import *
from sampler import *
from graph_optimisation import *


def get_dammy_struct_from_events_list(cogmap_events_ids_list, cogmap):
    # создаем матрицу полносвязного графа с вершинами в cogmap_events_ids и ребрами-расстояниями
    result_matrix_us = events_list_to_matrix(cogmap_events_ids_list, cogmap)

    # оптимизируем граф (строим остовное дерево)
    graph = get_optimized_graph(result_matrix_us, cogmap_events_ids_list)

    # обходим остовное дерево и одновременно заполняем dammy_struct, dammy_exemplar
    ids_gen = IdsGenerator()
    dammy_struct = Structure()
    dammy_exemplar = Exemplar(dammy_struct, cogmap)

    first_local_node_id = graph.recognition_order[0]
    point, mass, LUE_id = cogmap.get_event_data(local_event_id=first_local_node_id)
    first_dammy_global_node_id = ids_gen.generate_id()
    dammy_struct.add_node(global_node_id=first_dammy_global_node_id, u_from_parent=Point(0,0), parent_global_node_id=None,
                          mass=mass, LUE_id=LUE_id)
    dammy_exemplar.add_event_check_result_DAMMY(first_dammy_global_node_id, local_cogmap_id=first_local_node_id)

    for local_node_id in graph.recognition_order[1:]:
        parent_local_node_id = graph.get_parent_id(local_node_id)
        dammy_global_node_id = ids_gen.generate_id()

        parent_global_node_id = dammy_exemplar.get_global_id_by_local_id(parent_local_node_id)
        parent_point, _, _ = cogmap.get_event_data(parent_local_node_id)

        child_point, mass, LUE_id = cogmap.get_event_data(local_node_id)
        u_from_parent = Point(x=child_point.x - parent_point.x, y=child_point.y - parent_point.y)

        dammy_struct.add_node(global_node_id=dammy_global_node_id,
                              u_from_parent=u_from_parent, parent_global_node_id=parent_global_node_id,
                              mass=mass, LUE_id=LUE_id)
        dammy_exemplar.add_event_check_result_DAMMY(dammy_global_node_id, local_cogmap_id=local_node_id)

    return dammy_struct, dammy_exemplar


def events_list_to_matrix(cogmap_events_ids_list, cogmap):
    result_matrix_us = []
    for start_node_id in cogmap_events_ids_list:
        start_node_point = cogmap.get_point_of_event(start_node_id)
        us_array_for_this_start_node = get_all_u_data_for_start_node(start_node_point, cogmap_events_ids_list, cogmap)
        result_matrix_us.append(us_array_for_this_start_node)
    return result_matrix_us


def get_all_u_data_for_start_node(start_node_point, cogmap_events_ids_list, cogmap):
    result_array_us = []
    for end_node_id in cogmap_events_ids_list:
        end_node_point = cogmap.get_point_of_event(end_node_id)
        dist = my_dist(start_node_point, end_node_point)
        result_array_us.append(dist)
    return result_array_us


def get_hists_for_every_basic_node_of_struct(struct, cogmaps):
    m_dict = {}
    du_dict = {}

    for basic_global_event_id in struct.basic_nodes_ids:
        m_dict[basic_global_event_id] = []
        du_dict[basic_global_event_id] = []

    for cogmap in cogmaps:
        exemplar, basic_success = recognize_basic_struct(struct, cogmap)
        if basic_success:
            for basic_global_event_id in struct.basic_nodes_ids:
                rec_node = exemplar.get_node_recognition_res(basic_global_event_id)
                m_dict[basic_global_event_id].append(rec_node.mass)
                du_dict[basic_global_event_id].append(my_norm(rec_node.du))
    return m_dict, du_dict
