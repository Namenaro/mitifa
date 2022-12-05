# для данной эталонной когмапы генерим список n событий
# по списку событий создаем, как раньше, базовую структуру и отрисовываем ее экземпляр (если длина стр-ры меньше кол-ва событий, то костыльно брикаем эту итерацию)
# отображаем клссификационные свойства

from utils import *
from context import *
from train_utils import get_n_biggest_events
from visualise_objects import *
from visualise_top import *
from cogmap import *
from struct_builder import *
from f1 import eval_struct_f1

from random import randrange

def train_plan_A(context, logger, num_events=5):
    print("Creating new struct...")
    events_ids_list = get_n_biggest_events(context.etalon_map, num_events)
    dammy_struct, dammy_exemplar = get_dammy_struct_from_events_list(events_ids_list, cogmap=context.etalon_map)
    if len(dammy_struct) < num_events:
        logger.add_text("problem with Ilia code or not enough events in cogmap")
        return None

    logger.add_text("dammy экземпляр: ")
    fig = VIS_exemplar_as_graph(dammy_exemplar, need_annotations=False)
    logger.add_fig(fig)
    logger.save()


    struct_builder = BasicStructBuilder(dammy_struct, context, logger=None)
    result_basic_struct = struct_builder.get_basic_struct(need_relax=False, need_readress=False)
    print("Basic struct created...")

    logger.add_text(" Примеры распознавания на таргет-когмапах:")
    VIS_exemplars_of_struct(context.train_maps[1:4], result_basic_struct, logger)
    logger.save()

    fig = visualise_classification_properties_of_basic_struct(result_basic_struct, constrast_cogmaps=context.contrast_maps, target_cogmaps=context.train_maps)
    logger.add_text(" Классификационные свойства полученной базовой структуры:")
    logger.add_fig(fig)
    logger.save()

    F1 = eval_struct_f1(result_basic_struct, context)
    logger.add_text("F1 = " + str(F1))
    logger.save()
    return F1


if __name__ == '__main__':
    logger = HtmlLogger("LOG A PLAN mod")
    logger.add_text(" Простейшая политика добавления узла: выбираем n самых массифвных событий с эталона")

    class_nums_list = [200, 29, 1, 20, 8, 30, 50, 60, 90, 300, 234, 245, 152, 147, 96, 91, 43, 24, 12, 299,]
    num_pics = 0
    F1_sum =0
    for class_num in class_nums_list:
        #class_num = randrange(30)
        logger.add_line_little()
        logger.add_text("Символ " + str(class_num+1)) 
        context = get_default_context(class_num+1)
        F1 = train_plan_A(context, logger)
        if F1 is not None:
            F1_sum += F1
            num_pics +=1
    logger.add_text("Среднее F1 на этих данных равно " + str(F1_sum/num_pics))
    logger.save()
