from exemplar import *
from structure import *
from cogmap import *

from collections import namedtuple
from bisect import insort


ExemplarEntry = namedtuple('ExemplarEntry', ('exemplar', 'non_triviality'))

class BasicGenerationSorted:
    def __init__(self):
        self.entries = []

    def insert_new_exemplar(self, exemplar):
        non_triviality = exemplar.eval_exemplar()
        entry = ExemplarEntry(exemplar, non_triviality)
        insort(self.entries, entry, key=lambda x: -x.non_triviality)  # в порядке убывания

    def cut_extra_exemplars(self, surviving_max):
        if len(self.entries) > surviving_max:
            self.entries = self.entries[:surviving_max]

    def init_as_first_generation(self, structure, cogmap):
        global_node_id = structure.get_first_global_event_id()
        _, _, _, first_LUE_id, _ = structure.get_info_to_recognise_node(global_node_id)
        for local_event_id, LUECogmapEvent in cogmap.LUE_events.items():
            if LUECogmapEvent.LUE_id == first_LUE_id:
                exemplar = Exemplar(structure, cogmap)
                exemplar.add_event_check_result(global_node_id, LUECogmapEvent.local_cogmap_id)
                self.insert_new_exemplar(exemplar)

    def is_empty(self):
        if len(self.entries) == 0:
            return True
        return False

    def try_find_done_basic_exemplar(self):
        for exemplar_entry in self.entries:
            if exemplar_entry.exemplar.is_basic_recognition_done():
                return exemplar_entry.exemplar
        return None

    def __len__(self):
        return len(self.entries)
