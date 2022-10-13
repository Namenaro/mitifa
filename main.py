from visualise import *
from context import *
from LUE_rule import *
from cogmap import *



if __name__ == '__main__':
    logger = HtmlLogger("TRAIN LOG")
    # создаем начальный набор правил
    LUE_events_ids_gen = IdsGenerator()
    rule1 = LUERule(dx=0, dy=1, max_rad=5, is_horizontal=True, id_gen=LUE_events_ids_gen)
    rule2 = LUERule(dx=1, dy=0, max_rad=5, is_horizontal=False, id_gen=LUE_events_ids_gen)
    LUE_rules_list = [rule1, rule2]

    # создаем контекст
    context = Context(LUE_rules_list, class_num=147, contrast_sample_len=30)

    # отрисовываем пример когнитивной карты LUE-событий
    fig = VIS_LUE_cogmap1(cogmap=context.etalon_map)
    logger.add_fig(fig)
    logger.save()

    fig = VIS_LUE_cogmap(cogmap=context.etalon_map)
    logger.add_fig(fig)
    logger.save()

