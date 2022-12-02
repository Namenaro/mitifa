from context_utils import *
from LUE_rule import LUERule
from cogmap import LUECogmap


class Context:
    def __init__(self, LUE_rules_list, class_num=147, contrast_sample_len=1):
        self.class_num = class_num
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

    def get_more_contrast(self, num_cogmaps):
        new_contrast_pics = get_contrast(class_num=self.class_num, sample_len=num_cogmaps)
        new_contrast_maps = [LUECogmap(pic) for pic in new_contrast_pics]
        return new_contrast_maps


def get_default_context(class_num=135):
    LUE_events_ids_gen = IdsGenerator()
    rule1 = LUERule(dx=0, dy=1, max_rad=5, is_horizontal=True, id_gen=LUE_events_ids_gen)
    rule2 = LUERule(dx=1, dy=0, max_rad=5, is_horizontal=False, id_gen=LUE_events_ids_gen)
    LUE_rules_list = [rule1, rule2]

    context = Context(LUE_rules_list, class_num=class_num, contrast_sample_len=30)
    return context

if __name__ == '__main__':
    logger = HtmlLogger("TRAIN LOG")
    context = get_default_context()

