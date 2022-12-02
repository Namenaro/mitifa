from recognition_generation_exemplars import *
from structure import *
from exemplar import *
from utils import *
from visualise_objects import *

from copy import deepcopy
#-----------------------------------------------------------------
#  две основные пользовательские функции:
#-----------------------------------------------------------------

def recognize_experimental_struct(structure, cogmap, target_node_id):  # return best exemplar and succes|not_success
    best_basic_exemplar, basic_success = recognize_basic_struct(structure, cogmap)
    if basic_success:
        best_experimental_exemplar, non_basic_success = grow_non_basic_over_basic(best_basic_exemplar, target_node_id)
    else:
        best_experimental_exemplar = best_basic_exemplar

    experimental_succes = basic_success and non_basic_success
    return best_experimental_exemplar, experimental_succes


def recognize_basic_struct(structure, cogmap, logger=None):  # returns best basic exemplar and succes|not_success (either all nodes recognised or not all)
    GROW_MAX = 8
    SURVIVIVING_MAX = 12
    basic_success = True
    basic_non_success = False

    if logger is not None:
        logger.add_text("Recognition started, GROW_MAX=" + str(GROW_MAX) + ", SURVIVIVING_MAX=" + str(SURVIVIVING_MAX))

    current_generation = BasicGenerationSorted()
    current_generation.init_as_first_generation(structure, cogmap)
    next_generation = BasicGenerationSorted()

    if logger is not None:
        logger.add_text("First generation:")
        VIS_recognition_generation(logger, current_generation)
        VIS_nontrivs_of_generation(logger, current_generation)

    while True:
        # проверим критерий аварийного останова
        if current_generation.is_empty():
            return Exemplar(structure, cogmap), basic_non_success  # TODO надо вернуть луший из предыдущего поколения! для этого его сохранять

        # проверяем критерий хорошего останова
        best_done_basic_exemplar = current_generation.try_find_done_basic_exemplar()
        if best_done_basic_exemplar is not None:
            if logger is not None:
                logger.add_text("Succesfully recognised!")
            return best_done_basic_exemplar, basic_success

        # заполняем следующее поколение
        for exemplar_entry in current_generation.entries:
            children_exemplars_list = get_children_for_exemplar(exemplar_entry.exemplar, GROW_MAX)
            for child_exemplar in children_exemplars_list:
                next_generation.insert_new_exemplar(child_exemplar)

        # обрезаем размер следующего поколения (чтобы избежать взрыва)
        next_generation.cut_extra_exemplars(SURVIVIVING_MAX)

        # переключаем поколения
        current_generation = deepcopy(next_generation)
        next_generation = BasicGenerationSorted()

        if logger is not None:
            logger.add_text("updated and cutted new generation:")
            VIS_recognition_generation(logger, current_generation)
            VIS_nontrivs_of_generation(logger, current_generation)


#-----------------------------------------------------------------
# Вспомогательное:
#-----------------------------------------------------------------

def get_children_for_exemplar(exemplar, GROW_MAX): # наращивание на один шаг
    children_exemplars_list = []

    # делаем идеализированное предсказание:
    target_global_node_id, predicted_point, predicted_mass, predicted_LUE_id\
        = exemplar.make_prediction_for_next_event()


    # если уже есть связанное событие на карте, то результат распознавания однозначен
    target_local_event_id = exemplar.try_get_event_check_result_by_linked_event(target_global_node_id)
    if target_local_event_id is not None:
        child_exemplar = deepcopy(exemplar)
        child_exemplar.add_event_check_result(target_global_node_id, target_local_event_id)
        return [child_exemplar]

    # находим не более GROW_MAX кандидатов на его результат проверки
    # причем событий-кандидатов проверяем, не учтено ли оно уже в этом экземпляре
    local_evends_list = exemplar.get_no_more_MAX_events_around_point_by_LUE(predicted_point, predicted_LUE_id, GROW_MAX)
    for local_event in local_evends_list:
        child_exemplar = deepcopy(exemplar)
        child_exemplar.add_event_check_result(target_global_node_id, local_event.local_cogmap_id)
        children_exemplars_list.append((child_exemplar))
    return children_exemplars_list


def grow_non_basic_over_basic(exemplar, target_node_id):
    all_success = True
    all_non_success = False

    while True:
        # делаем идеализированное предсказание:
        target_global_node_id, predicted_point, predicted_mass, predicted_LUE_id \
                = exemplar.make_prediction_for_next_event()

        # если уже есть связанное событие на карте, то результат распознавания однозначен
        target_local_event_id = exemplar.try_get_event_check_result_by_linked_event(target_global_node_id)
        if target_local_event_id is not None:
            exemplar.add_event_check_result(target_global_node_id, target_local_event_id)
            return exemplar, all_success

        local_events_list = exemplar.get_no_more_MAX_events_around_point_by_LUE(predicted_point,
                                                                                       predicted_LUE_id, MAX=1)
        if len(local_events_list) == 0:
            return exemplar, all_non_success

        exemplar.add_event_check_result(target_global_node_id, local_events_list[0].local_cogmap_id)
        if target_global_node_id == target_node_id:
            return exemplar, all_success