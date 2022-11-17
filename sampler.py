from structure import *
from context import *
from utils import *
from recognise import *

from random import choice, randint

def sample_event_by_LUE_and_mass(contrast_maps, LUE_id, mass):
    SAMPLE_SIZE = 100
    ATTEMTS = 1000

    found_LUE_events = []
    sample_masses = []
    sample_dus = []

    attempts_counter = 0
    while True:
        # выбираем случайную картинку, на ней случайную точку
        # в окрестности этой точки ищем ближайшее событие с нужным LUE_id
        # записываем его массу, расстояние до него (если только оно уже не попало в выборку)
        cogmap = choice(contrast_maps)
        x = randint(0, cogmap.pic.shape[0])
        y = randint(0, cogmap.pic.shape[0])
        point = Point(x, y)
        LUE_events_list = cogmap.get_no_more_events_around_point_by_LUE(point, LUE_id, MAX_EVENTS=1, exclusions=[])
        if len(LUE_events_list) > 0:
            found_LUE_event = LUE_events_list[0]
            if found_LUE_event not in found_LUE_events:
                found_LUE_events.append(found_LUE_event)
                sample_masses.append(found_LUE_event.mass)
                du = my_dist(found_LUE_event.point, point)
                sample_dus.append(du)

        if len(found_LUE_events) == SAMPLE_SIZE or attempts_counter == ATTEMTS:
            break
        attempts_counter += 1

    return sample_masses, sample_dus


def sample_struct(train_maps, basic_struct):
    exemplars = []
    for cogmap in train_maps:
        best_done_basic_exemplar, basic_success = recognize_basic_struct(basic_struct, cogmap)
        if basic_success:
            exemplars.append(best_done_basic_exemplar)
    return exemplars

def sample_experimental_node(train_maps, exparimental_struct, target_node_id):
    exp_node_masses_sample = []
    exp_node_dus_sample = []
    for cogmap in train_maps:
        best_experimental_exemplar, experimental_succes = recognize_experimental_struct(exparimental_struct, cogmap, target_node_id)
        if experimental_succes:
            node_recognition_res = best_experimental_exemplar.get_node_recognition_res(target_node_id)
            du = my_norm(node_recognition_res.du)
            exp_node_dus_sample.append(du)
            exp_node_masses_sample.append(node_recognition_res.mass)

    return exp_node_masses_sample, exp_node_dus_sample

def sample_non_triviality_values_for_basic_struct(basic_struct, cogmaps_dataset):
    non_triviality_values = []
    for cogmap in cogmaps_dataset:
        best_experimental_exemplar, _ = recognize_basic_struct(basic_struct, cogmap=cogmap)
        non_triviality_value = best_experimental_exemplar.eval_exemplar()
        non_triviality_values.append(non_triviality_value)
    return non_triviality_values