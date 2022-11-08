from context import *
from visualise import *
from cogmap import *
from struct_builder import *

def manual_train():
    # Служебное:
    logger = HtmlLogger("TRAIN LOG")
    context = get_default_context()

    # отрисовываем пример когнитивной карты LUE-событий
    VIS_LUE_cogmap1(cogmap=context.etalon_map, logger=logger)
    VIS_LUE_cogmap(cogmap=context.etalon_map, logger=logger)


    # вручную заданный список событий на context.etalon_map
    events_ids_list =[0,2,8]
    logger.add_text(" Вручную выбраны события: " + str(events_ids_list))


    # обучаем структуру на этих событиях:
    dammy_struct, dammy_exemplar = get_dammy_struct_from_events_list(events_ids_list, cogmap=context.etalon_map)
    struct_builder = BasicStructBuilder(dammy_struct, dammy_exemplar, context, logger)
    result_basic_struct = struct_builder.get_basic_struct()

    # оцениваем обученную структуру:
    VIS_struct_recognise(result_basic_struct, context, logger)
    VIS_struct_evaluation(result_basic_struct, context, logger)



if __name__ == '__main__':
    manual_train()

