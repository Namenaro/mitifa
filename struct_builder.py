from structure import *
from exemplar import *
from context import *
from cogmap import *
from sampler import *
from struct_builder_utils import get_dammy_struct_from_events_list
from hists import Hist
from struct_relaxer import StructRelaxer
from utils import *
from visualise import *


class BasicStructBuilder:
    def __init__(self, dammy_struct, context, logger):
        self.result_struct = Structure()
        self.dammy_struct = dammy_struct
        self.context = context
        self.logger = logger

    def init_first_base_node(self):
        first_node_id = self.dammy_struct.recognition_order[0]
        parent_global_node_id, u_from_parent, mass, LUE_id= self.dammy_struct.get_info_to_recognise_node(first_node_id)
        sample_masses, sample_dus = sample_event_by_LUE_and_mass(self.context.contrast_maps, LUE_id, mass)
        actual_m_hist = Hist(sample_masses)
        actual_du_hist = Hist(sample_dus)
        self.result_struct.add_node(first_node_id, u_from_parent, parent_global_node_id, mass, LUE_id, actual_m_hist=actual_m_hist, actual_du_hist=actual_du_hist)


    def get_basic_struct(self, need_relax, need_readress):
        # создаем первое базовое событие, беря за основу небазовое первое событие из dammy_struct, по которой мы строим сейчас базовую стр-ру
        self.init_first_base_node()

        j=1
        self.logger.add_text("Добавление " + str(j) + "-ой ноды в растущую стрктуру:")
        self.logger.add_fig(VIS_struct_as_graph(self.result_struct))
        VIS_nodes_info_struct(self.result_struct, logger=self.logger)
        self.logger.add_line_little()

        # перебираем все события self.dammy_struct кроме первого
        for node_global_id in self.dammy_struct.recognition_order[1:]:
            j+=1
            self.logger.add_text("Добавление " + str(j) + "-ой ноды в растущую стрктуру:")
            # добавляем новый experimental узел из self.dammy_struct в реузльтирующую структуру
            parent_global_node_id, u_from_parent, mass, LUE_id = self.dammy_struct.get_info_to_recognise_node(node_global_id)
            self.result_struct.add_node(node_global_id, u_from_parent, parent_global_node_id, mass, LUE_id)

            # для него получаем выбоки, обусловленные на всю уже построенную базовую структуру (она = текущая self.result_struct)
            exp_node_masses_sample, exp_node_dus_sample = sample_experimental_node(self.context.train_maps, self.result_struct, target_node_id=node_global_id)

            # делаем этот узел базовым:
            actual_m_hist = Hist(exp_node_masses_sample)
            actual_du_hist = Hist(exp_node_dus_sample)
            self.result_struct.nodes_dict[node_global_id].actual_m_hist =actual_m_hist
            self.result_struct.nodes_dict[node_global_id].actual_du_hist = actual_du_hist

            self.logger.add_text(" полученная не релаксированная версия базовой части структуры :")
            self.logger.add_fig(VIS_struct_as_graph(self.result_struct))
            VIS_nodes_info_struct(self.result_struct, logger=self.logger)


            if need_relax:
                # релаксиурем имеющуюся к этому моменту базовую структуру
                dispersional_relaxer = StructRelaxer(basic_struct=self.result_struct, context=self.context)
                dammy_struct = dispersional_relaxer.get_relaxed_dammy_struct()

                self.logger.add_text("После релаксации базовой части получена ее дамми-версия: ")
                self.logger.add_fig(VIS_struct_as_graph(self.result_struct))
                self.logger.save()

                # реузльтаты релаксации из переносим в result_struct
                for node_id, node_exemplar in self.dammy_struct.items():
                    self.result_struct.nodes_dict[node_id].u_from_parent = node_exemplar.u_from_parent
                    self.result_struct.nodes_dict[node_id].parent_global_node_id = node_exemplar.parent_global_node_id
                    self.result_struct.nodes_dict[node_id].mass = node_exemplar.mass


                self.logger.add_text("Релаксированная версия базовой части структуры :")
                self.logger.add_fig(VIS_struct_as_graph(self.result_struct))
                self.logger.save()


                if need_readress:
                    # делаем ре-адрессинг неучтенных узлов относительно учтенных:
                    for parent_id in dammy_struct.recognition_order:
                        # ищем в dammy_struct всех детей этого родителя, которые не учтены
                        for child_node_id, node_exemplar in self.dammy_struct.items():
                            if node_exemplar.parent_global_node_id == parent_id:
                                if child_node_id not in dammy_struct.recognition_order:
                                    # считаем изменение координаты родителя (относительно его родителя) после релаксации:
                                    new_parent_coord = dammy_struct.nodes_dict[parent_id].u_from_parent
                                    old_parent_coord = self.result_struct.nodes_dict[parent_id].u_from_parent
                                    du = Point(new_parent_coord.x-old_parent_coord.x, new_parent_coord.y-old_parent_coord.y)

                                    # это изменение вычитаем из координат ребенка и записываем это в дамми-структуру
                                    old_child_coord = self.dammy_struct.nodes_dict[child_node_id].u_from_parent
                                    new_child_coord = old_child_coord+du
                                    self.dammy_struct.nodes_dict[child_node_id].u_from_parent = new_child_coord

                    self.logger.add_text("После реадрессинга детей дамми-структура выглядит так:")
                    self.logger.add_fig(VIS_struct_as_graph(self.dammy_struct))
                    self.logger.save()
                else:
                    self.logger.add_text("Реадрессинг детей в дамми-структуре отключен...")

        return self.result_struct



