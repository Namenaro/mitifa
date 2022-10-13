from context_utils import *
from LUE_rule import LUERule
from cogmap import LUECogmap


class Context:
    def __init__(self, LUE_rules_list, class_num=147, contrast_sample_len=1):
        etalon_pic, train_pics, test_pics, contrast_pics = get_all_pics_for_training(class_num, contrast_sample_len)
        self.LUE_rules = []

        self.etalon_map = LUECogmap(etalon_pic)

        self.train_maps = []
        self.test_maps = []
        self.contrast_maps = []

        for pic in train_pics:
            self.train_maps.append(LUECogmap(pic))
        for pic in test_pics:
            self.test_maps.append(LUECogmap(pic))
        for pic in contrast_pics:
            self.contrast_maps.append(LUECogmap(pic))

        for rule in LUE_rules_list:
            self.add_new_rule(rule)

    def add_new_rule(self, rule):
        self.LUE_rules.append(rule)

        self.etalon_map.update_by_LUE_rule(rule)

        for map in self.train_maps:
            map.update_by_LUE_rule(rule)
        for map in self.test_maps:
            map.update_by_LUE_rule(rule)
        for map in self.contrast_maps:
            map.update_by_LUE_rule(rule)
