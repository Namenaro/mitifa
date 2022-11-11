from context import *
from visualise import *
from cogmap import *
from struct_builder import *

def manual_train():
    # Служебное:
    logger = HtmlLogger("TRAIN LOG")
    context = get_default_context()

    # отрисовываем пример когнитивной карты LUE-событий
    VIS_LUE_cogmap_first_generation(cogmap=context.etalon_map, logger=logger)
    VIS_LUE_cogmap_second_generation(cogmap=context.etalon_map, logger=logger)


    # вручную заданный список событий на context.etalon_map
    events_ids_list = [0, 2, 8]
    logger.add_text(" Вручную выбраны события: " + str(events_ids_list))


    # по одному образцу создаем " дамми" структуру и соотв. ей экземпляр:
    dammy_struct, dammy_exemplar = get_dammy_struct_from_events_list(events_ids_list, cogmap=context.etalon_map)

    logger.add_line_little()
    logger.add_text("По одному образцу создаем dammy структуру и соотв. ей dammy экземпляр;")
    logger.add_text("dammy структура:")
    fig = VIS_struct_as_graph(dammy_struct)
    logger.add_fig(fig)
    logger.add_text("dammy экземпляр: ")
    fig = VIS_exemplar_as_graph(dammy_exemplar, need_annotations=True)
    logger.add_fig(fig)

    # Выращиваем базовую структуру по dammy структуре:
    logger.add_line_big()
    logger.add_text("Выращиваем базовую структуру по dammy структуре...")
    struct_builder = BasicStructBuilder(dammy_struct, dammy_exemplar, context, logger)
    result_basic_struct = struct_builder.get_basic_struct()


    # оцениваем обученную структуру:--------------------------------------------------------
    logger.add_line_big()

    fig = VIS_struct_as_graph(result_basic_struct)
    logger.add_text(" Итоговая боазовая структура выглядит так:")
    logger.add_fig(fig)
    logger.save()

    fig = visualise_classification_properties_of_basic_struct(result_basic_struct, constrast_cogmaps=context.contrast_maps, target_cogmaps=context.train_maps)
    logger.add_text(" Классификационные свойства полученной базовой структуры:")
    logger.add_fig(fig)
    logger.save()

    logger.add_text(" Примеры распознавания на таргет-когмапах:")
    VIS_exemplars_of_struct(context.train_maps, result_basic_struct, logger)
    logger.save()

    logger.add_text(" Примеры распознавания на констрастных-когмапах:")
    VIS_exemplars_of_struct(context.contrast_maps, result_basic_struct, logger)
    logger.save()

    logger.add_text(" Подробный пример распознавания:")
    VIS_detailed_exemplar_of_struct(context.train_maps[1], result_basic_struct, logger)
    logger.save()


if __name__ == '__main__':
    manual_train()

