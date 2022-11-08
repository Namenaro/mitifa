from collections import namedtuple
from bisect import insort
from copy import deepcopy

from structure import *
from exemplar import *


#-----------------------------------------------------------------
#  две основные пользовательские функции:
#-----------------------------------------------------------------

def recognize_experimental_struct(structure, cogmap):  # return best exemplar and succes|not_success
    best_basic_exemplar, basic_success = recognize_basic_struct(structure, cogmap)
    if basic_success:
        best_experimental_exemplar, non_basic_success = grow_non_basic_over_basic(best_basic_exemplar)

    experimental_succes = basic_success and non_basic_success
    return best_experimental_exemplar, experimental_succes


def recognize_basic_struct(structure, cogmap):  # returns best basic exemplar and succes|not_success (either all nodes recognised or not all)
    GROW_MAX = 3
    SURVIVIVING_MAX = 5
    basic_success = True
    basic_non_success = False

    prev_generation = BasicGenerationSorted()
    current_generation = BasicGenerationSorted()
    current_generation.init_as_first_generation(structure, cogmap)
    next_generation = BasicGenerationSorted()

    while True:
        # проверим критерий аварийного останова
        if current_generation.is_empty():
            if prev_generation.is_empty():
                return Exemplar(structure, cogmap), basic_non_success
            return prev_generation.get_best_exemplar(), basic_non_success

        # проверяем критерий хорошего останова
        best_done_basic_exemplar = current_generation.try_find_done_basic_exemplar()
        if best_done_basic_exemplar is not None:
            return best_done_basic_exemplar, basic_success

        # заполняем следующее поколение
        for exemplar in current_generation.exemplars:
            children_exemplars_list = get_children_for_exemplar(exemplar, GROW_MAX)
            for child_exemplar in children_exemplars_list:
                next_generation.insert_new_exemplar(child_exemplar)

        # обрезаем размер следующего поколения (чтобы избежать взрыва)
        next_generation.cut_extra_exemplars(SURVIVIVING_MAX)

        # переключаем поколения
        prev_generation = current_generation
        current_generation = next_generation
        next_generation = BasicGenerationSorted()


#-----------------------------------------------------------------
# Вспомогательное:
#-----------------------------------------------------------------
ExemplarEntry = namedtuple('ExemplarEntry', ('exemplar', 'non_triviality'))

class BasicGenerationSorted:
    def __init__(self):
        self.entries = []

    def insert_new_exemplar(self, exemplar):
        non_triviality = exemplar.eval_exemplar()
        entry = ExemplarEntry(exemplar, non_triviality)
        insort(self.entries, entry, key=lambda x: -x.non_triviality) # в порядке убывания

    def cut_extra_exemplars(self, surviving_max):
        if len(self.entries) > surviving_max:
            self.entries = self.entries[:surviving_max]

    def init_as_first_generation(self, structure, cogmap):
        global_node_id = structure.get_first_global_event_id()
        _, _, _, first_LUE_id = structure.get_info_to_recognise_node(global_node_id)
        for local_event_id, LUECogmapEvent in cogmap.LUE_events.items():
            if LUECogmapEvent.LUE_id == first_LUE_id:
                exemplar = Exemplar(structure, cogmap)
                exemplar.add_event_check_result(global_node_id, LUECogmapEvent.local_cogmap_id)
                self.insert_new_exemplar(exemplar)

    def is_empty(self):
        if len(self.exemplars) == 0:
            return True
        return False

    def try_find_done_basic_exemplar(self):
        for exemplar_entry in self.entries:
            if exemplar_entry.exemplar.is_basic_recognition_done():
                return exemplar_entry.exemplar
        return None


def get_children_for_exemplar( exemplar, GROW_MAX): # наращивание на один шаг
    children_exemplars_list = []

    # делаем идеализированное предсказание:
    target_global_node_id, predicted_point, predicted_mass, predicted_LUE_id\
        = exemplar.make_prediction_for_next_event()

    # находим не более GROW_MAX кандидатов на его результат проверки
    # причем событий-кандидатов проверяем, не учтено ли оно уже в этом экземпляре
    local_evends_ids_list = exemplar.get_no_more_MAX_events_around_point_by_LUE(predicted_point, predicted_LUE_id, GROW_MAX)
    for local_evend_id in local_evends_ids_list:
        child_exemplar = deepcopy(exemplar)
        child_exemplar.add_event_check_result(target_global_node_id, local_evend_id)
    return children_exemplars_list


def grow_non_basic_over_basic(exemplar):
    all_success = True
    all_non_success = False

    while True:
        if exemplar.is_recognition_done():
            return exemplar, all_success

        # делаем идеализированное предсказание:
        target_global_node_id, predicted_point, predicted_mass, predicted_LUE_id \
                = exemplar.make_prediction_for_next_event()

        local_events_ids_list = exemplar.get_no_more_MAX_events_around_point_by_LUE(predicted_point,
                                                                                       predicted_LUE_id, MAX=1)
        if len(local_events_ids_list) == 0:
            return exemplar, all_non_success

        exemplar.add_event_check_result(target_global_node_id, local_events_ids_list[0])
