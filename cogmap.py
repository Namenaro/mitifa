from utils import *
from LUE_rule import LUERule
from cogmap_utils import *

class LUECogmapEvent:
    def __init__(self, seq, LUE_id, is_horizonral, point, local_cogmap_id, cogmap):
        self.cogmap = cogmap
        self.seq = seq # [Point, Point,...]
        self.LUE_id = LUE_id
        self.local_cogmap_id = local_cogmap_id
        self.intersects_ids =  [] # другие ЛУЕ-события с карты, с которыми это имеет персечение по первичным событиям
        self.is_horizontal = is_horizonral
        self.point = point
        self.mass = len(self.seq)

    def add_intersection(self, id_in_cogmap):
        self.intersects_ids.append(id_in_cogmap)

    def has_intersection(self, other_event):
        if other_event.is_horizontal != self.is_horizontal:
            return False
        for point in other_event.seq:
             if point in self.seq:
                 return True
        return False

    def __eq__(self, other):
        return self.cogmap == other.cogmap and self.local_cogmap_id == other.local_cogmap_id


class LUECogmap:
    def __init__(self, pic):
        self.pic = pic
        self.hor_img = None
        self.ver_img = None
        self._fill_hor_ver()

        self.local_ids_gen = IdsGenerator()
        self.points_to_events = {}  # {point:  [LUECogmapEvent] }
        self.LUE_events = {} # {local_event_id:  LUECogmapEvent }

    def __eq__(self, other):
        return self.pic == other.pic

    def _fill_hor_ver(self):
        rule_hor = LUERule(dx=1, dy=0, max_rad=1)
        rule_ver = LUERule(dx=0, dy=1, max_rad=1)
        seqs_hor = rule_hor.apply_to_binary_map(self.pic)
        seqs_ver = rule_ver.apply_to_binary_map(self.pic)
        self.hor_img = seqs_starts_to_binary_map(map_shape=self.pic.shape, seqs=seqs_hor)
        self.ver_img = seqs_starts_to_binary_map(map_shape=self.pic.shape, seqs=seqs_ver)


    def _register_LUE_event(self, new_LUE_event):
        for old_local_event_id, old_LUE_event in self.LUE_events.items():
            if new_LUE_event.has_intersection(old_LUE_event):
                old_LUE_event.add_intersection(new_LUE_event.local_cogmap_id)
                new_LUE_event.add_intersection(old_LUE_event.local_cogmap_id)
        self.LUE_events[new_LUE_event.local_cogmap_id]=new_LUE_event
        if new_LUE_event.point not in  self.points_to_events.keys():
            self.points_to_events[new_LUE_event.point]=[]
        self.points_to_events[new_LUE_event.point].append(new_LUE_event)


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
                                             local_cogmap_id=self.local_ids_gen.generate_id(),
                                             cogmap=self)
                end_event = LUECogmapEvent(seq, LUE_id=rule.end_LUE_id,
                                           is_horizonral=rule.is_horizontal,
                                           point=seq[0],
                                           local_cogmap_id=self.local_ids_gen.generate_id(),
                                           cogmap=self)
                self._register_LUE_event(start_event)
                self._register_LUE_event(end_event)

    def get_event_data(self, local_event_id):
        lue_event = self.LUE_events[local_event_id]
        point = lue_event.point
        mass = lue_event.mass
        LUE_id = lue_event.LUE_id
        return point, mass, LUE_id

    def get_point_of_event(self, local_event_id):
        lue_event = self.LUE_events[local_event_id]
        point = lue_event.point
        return point

    def get_LUE_cogmap_event(self, local_event_id):
        return self.LUE_events[local_event_id]

    def get_no_more_events_around_point_by_LUE(self, point, LUE_id, MAX_EVENTS, exclusions):
        result_events_ids_list = []
        MAX_RADIUS = 50
        for radius in range(0, MAX_RADIUS+1):
            candidate_points = get_coords_for_radius(center=point, radius=radius)
            for candidate_point in candidate_points:
                lue_cogmap_events_list_in_point = self.points_to_events.get(candidate_point, None)
                if lue_cogmap_events_list_in_point is not None:
                    for lue_cogmap_event in lue_cogmap_events_list_in_point:
                        if lue_cogmap_event.LUE_id == LUE_id:
                            if lue_cogmap_event.local_cogmap_id not in exclusions:
                                result_events_ids_list.append(lue_cogmap_event.local_cogmap_id)
                                if len(result_events_ids_list) == MAX_EVENTS:
                                    break
        return result_events_ids_list