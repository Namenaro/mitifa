from utils import *
from LUE_rule import LUERule
from cogmap_utils import *

class LUECogmapEvent:
    def __init__(self, seq, LUE_id, is_horizonral, point, local_cogmap_id):
        self.seq = seq # [Point, Point,...]
        self.LUE_id = LUE_id
        self.local_cogmap_id = local_cogmap_id
        self.intersects_ids =  [] # другие ЛУЕ-события с карты, с которыми это имеет персечение по первичным событиям
        self.is_horizontal = is_horizonral
        self.point = point


    def get_mass(self):
        return len(self.seq)

    def add_intersection(self, id_in_cogmap):
        self.intersects_ids.append(id_in_cogmap)

    def has_intersection(self, other_event):
        if other_event.is_horizontal != self.is_horizontal:
            return False
        for point in other_event.seq:
             if point in self.seq:
                 return True
        return False


class LUECogmap:
    def __init__(self, pic):
        self.pic = pic
        self.hor_img = None
        self.ver_img = None
        self._fill_hor_ver()

        self.local_ids_gen = IdsGenerator()
        self.points_to_events = {}  # {point:  LUECogmapEvent }
        self.LUE_events_list=[]


    def _fill_hor_ver(self):
        rule_hor = LUERule(dx=1, dy=0, max_rad=1)
        rule_ver = LUERule(dx=0, dy=1, max_rad=1)
        seqs_hor = rule_hor.apply_to_binary_map(self.pic)
        seqs_ver = rule_ver.apply_to_binary_map(self.pic)
        self.hor_img = seqs_starts_to_binary_map(map_shape=self.pic.shape, seqs=seqs_hor)
        self.ver_img = seqs_starts_to_binary_map(map_shape=self.pic.shape, seqs=seqs_ver)


    def _register_LUE_event(self, new_LUE_event):
        for old_LUE_event in self.LUE_events_list:
            if new_LUE_event.has_intersection(old_LUE_event):
                old_LUE_event.add_intersection(new_LUE_event.local_cogmap_id)
                new_LUE_event.add_intersection(old_LUE_event.local_cogmap_id)
        self.LUE_events_list.append(new_LUE_event)
        self.points_to_events[new_LUE_event.point]=new_LUE_event


    def update_by_LUE_rule(self, rule):
        if rule.is_horizontal:
            found_seqs = rule.apply_to_binary_map(self.hor_img)
        else:
            found_seqs = rule.apply_to_binary_map(self.ver_img)

        if len(found_seqs) > 0:
            for seq in found_seqs:

                start_event = LUECogmapEvent(seq, LUE_id=rule.start_LUE_id,
                                             is_horizonral=rule.is_horizontal,
                                             point=seq[-1],
                                             local_cogmap_id=self.local_ids_gen.generate_id())
                end_event = LUECogmapEvent(seq, LUE_id=rule.end_LUE_id,
                                           is_horizonral=rule.is_horizontal,
                                           point=seq[0],
                                           local_cogmap_id=self.local_ids_gen.generate_id())
                self._register_LUE_event(start_event)
                self._register_LUE_event(end_event)
